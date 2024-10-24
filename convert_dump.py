# задать
#   exePath
#   modsPath
# мод из папки "mod.ignore" скопируется в папку с игрой (потом удалится)
# data.raw -> json

from pathlib import Path
import shutil
import psutil
import subprocess
import json

exePath = Path("D:/Games/Factorio_2_SA/bin/x64/factorio.exe")
modsPath = Path("D:/Games/Factorio_2_SA/mods")


def get_json_from_factorio(json_filename):

    # the source directory of the mod
    src_mod_dir = Path("mod.ignore/foremanexport_1.0.0")

    modPath = modsPath / "foremanexport_1.0.0"
    if modPath.exists():
        shutil.rmtree(modPath)
    modPath.mkdir()

    # copy the files as necessary
    # copy mod files
    shutil.copyfile(src_mod_dir / "info.json", modPath / "info.json")
    shutil.copyfile(
        src_mod_dir / "instrument-after-data.lua",
        modPath / "instrument-after-data.lua",
    )
    # recipe&technology difficulties each have their own lua script
    # Recipe difficulty - Normal or Expensive
    # Technology difficulty - Normal or Expensive
    # Recipe = Normal, Technology = Normal
    shutil.copyfile(
        src_mod_dir / "instrument-control - nn.lua",
        modPath / "instrument-control.lua",
    )

    # launch factorio to create the temporary save we will use for export (LAUNCH #1)
    print("run 1")
    command = [str(exePath)]
    command.extend(["--mod-directory", str(modsPath)])
    command.extend(["--create", "temp-save.zip"])
    process = psutil.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    # for line in out.decode("utf-8").split("\n"):
    #     line = line.rstrip()
    #     print(line)
    # print("err=", err.decode("utf-8"))

    # launch factorio again to export the data (LAUNCH #2)
    print("run 2")
    command = [str(exePath)]
    command.extend(["--mod-directory", str(modsPath)])
    command.extend(["--instrument-mod", "foremanexport"])
    command.extend(["--benchmark", "temp-save.zip"])
    command.extend(["--benchmark-ticks", "1"])
    command.extend(["--benchmark-runs", "1"])
    process = psutil.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()

    #             string dataString = resultString.Substring(resultString.IndexOf("<<<START-EXPORT-P2>>>") + 23);
    #             dataString = dataString.Substring(0, dataString.IndexOf("<<<END-EXPORT-P2>>>") - 2);

    dataString = ""
    get_dataString = False
    for line in out.decode("utf-8").split("\n"):
        line = line.rstrip()

        # get json data
        if "<<<END-EXPORT-P2>>>" in line:
            get_dataString = False

        if get_dataString:
            dataString += line

        if "<<<START-EXPORT-P2>>>" in line:
            get_dataString = True

    print("err=", err.decode("utf-8"))

    shutil.rmtree(modPath)
    Path("temp-save.zip").unlink(missing_ok=False)

    # dataString -> json
    json_data = json.loads(dataString)
    json_str = json.dumps(
        json_data,
        separators=(",", ":"),
        indent=4,
        ensure_ascii=False,
        sort_keys=True,
    )
    with open(json_filename, "w", encoding="utf8") as f:
        print(json_str, file=f, flush=True)


#             string lnamesString = resultString.Substring(resultString.IndexOf("<<<START-EXPORT-LN>>>") + 23);
#             lnamesString = lnamesString.Substring(0, lnamesString.IndexOf("<<<END-EXPORT-LN>>>") - 2);
#             lnamesString = lnamesString.Replace("\n", "").Replace("\r", "").Replace("<#~#>", "\n");

#             string iconString = resultString.Substring(resultString.IndexOf("<<<START-EXPORT-P1>>>") + 23);
#             iconString = iconString.Substring(0, iconString.IndexOf("<<<END-EXPORT-P1>>>") - 2);


#             string[] lnames = lnamesString.Split('\n'); //keep empties - we know where they are!
#             Dictionary<string, string> localisedNames = new Dictionary<string, string>(); //this is the link between the 'lid' property and the localised names in dataString
#             for (int i = 0; i < lnames.Length / 2; i++)
#                 localisedNames.Add('$' + i.ToString(), lnames[(i * 2) + 1].Replace("Unknown key: \"", "").Replace("\"", ""));

# #if DEBUG
#             File.WriteAllText(Path.Combine(Application.StartupPath, "_iconJObjectOut.json"), iconString.ToString());
#             File.WriteAllText(Path.Combine(Application.StartupPath, "_dataJObjectOut.json"), dataString.ToString());
# #endif
#             JObject iconJObject = null;
#             JObject dataJObject = null;
#             try
#             {
#                 iconJObject = JObject.Parse(iconString); //this is what needs to be parsed to get all the icons
#                 dataJObject = JObject.Parse(dataString); //this is pretty much the entire json preset - just need to save it.
#             }
#             catch
#             {
#                 MessageBox.Show("Foreman export could not be completed - unknown json parsing error.\nSorry");
#                 ErrorLogging.LogLine("json parsing of output failed. This is clearly an error with the export mod (foremanexport_1.0.0). Consult _iconJObjectOut.json and _dataJObjectOut.json and check which one isnt a valid json (and why)");
#                 File.WriteAllText(Path.Combine(Application.StartupPath, "_iconJObjectOut.json"), iconString.ToString());
#                 File.WriteAllText(Path.Combine(Application.StartupPath, "_dataJObjectOut.json"), dataString.ToString());
#                 CleanupFailedImport(modsPath);
#                 return "";
#             }

#             //now to trawl over the dataJObject entities and replace any 'lid' with 'localised_name'
#             foreach (JToken set in dataJObject.Values().ToList())
#             {
#                 foreach (JToken obj in set.ToList())
#                 {
#                     if (obj is JObject jobject && (string)jobject["lid"] != null)
#                     {
#                         JProperty lname = new JProperty("localised_name", localisedNames[(string)jobject["lid"]]);
#                         jobject.Add(lname);
#                         jobject.Remove("lid");
#                     }
#                 }
#             }

#             //save new preset (data)
#             File.WriteAllText(Path.Combine(Application.StartupPath, presetPath + ".pjson"), dataJObject.ToString(Formatting.Indented));
#             File.Copy(Path.Combine(Application.StartupPath, "baseCustom.json"), Path.Combine(Application.StartupPath, presetPath + ".json"), true);
# #if DEBUG
#             File.WriteAllText(Path.Combine(Application.StartupPath, "_iconJObjectOut.json"), iconJObject.ToString(Formatting.Indented));
#             File.WriteAllText(Path.Combine(Application.StartupPath, "_dataJObjectOut.json"), dataJObject.ToString(Formatting.Indented));
# #endif

#             if (token.IsCancellationRequested)
#             {
#                 process.Close();
#                 CleanupFailedImport(modsPath);
#                 return "";
#             }

#             //now we need to process icons. This is done by the IconProcessor.
#             Dictionary<string, string> modSet = new Dictionary<string, string>();
#             foreach (var objJToken in dataJObject["mods"].ToList())
#                 modSet.Add(((string)objJToken["name"]).ToLower(), (string)objJToken["version"]);

#             using (IconCacheProcessor icProcessor = new IconCacheProcessor())
#             {
#                 if (!icProcessor.PrepareModPaths(modSet, modsPath, Path.Combine(installPath, "data"), token))
#                 {
#                     if (!token.IsCancellationRequested)
#                     {
#                         MessageBox.Show("Mod inconsistency detected. Try to see if launching Factorio gives an error?");
#                         ErrorLogging.LogLine("Mod parsing failed - the list of mods provided could not be mapped to the existing mod folders & zip files.");
#                     }
#                     CleanupFailedImport(modsPath, presetPath);
#                     return "";
#                 }

#                 if (!icProcessor.CreateIconCache(iconJObject, Path.Combine(Application.StartupPath, presetPath + ".dat"), progress, token, 30, 100))
#                 {
#                     if (!token.IsCancellationRequested)
#                     {
#                         ErrorLogging.LogLine(string.Format("{0}/{1} images were not found while processing icons.", icProcessor.FailedPathCount, icProcessor.TotalPathCount));
#                         if (MessageBox.Show(string.Format("{0}/{1} images that were processed for icons were not found and thus some icons are likely wrong/empty. Do you still wish to continue with the preset import?", icProcessor.FailedPathCount, icProcessor.TotalPathCount), "Confirm Preset Import", MessageBoxButtons.YesNo) != DialogResult.Yes)
#                         {
#                             CleanupFailedImport(modsPath, presetPath);
#                             return "";
#                         }
#                     }
#                     else
#                     {
#                         CleanupFailedImport(modsPath, presetPath);
#                         return "";
#                     }
#                 }
#             }

#             SetStateForemanExportMod(modsPath, false);
#             return NewPresetName;
#         });
#     }


######################################
#
# main
if __name__ == "__main__":

    get_json_from_factorio("Factorio 2.0 SA Vanilla.json")
