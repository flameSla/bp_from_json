import os
from bp_from_json import blueprint
from bp_from_json import entity
from bp_from_json import dict_bp


################################################################
def input_def(text, default):
    str = input(text + "[" + default + "]:")
    return str if str else default


################################################################
def combine_requests_from_chests(bp):
    new_bp = blueprint.new_blueprint()
    req = dict_bp()
    for e in bp.get_entities():
        if "logistic-chest-requester" in e.read_name():
            req += e.get_request_filters()
    print("req = ", type(req), req)
    new_entity = entity.new_entity("logistic-chest-requester", 0, 0)
    new_entity.append_request_filters(req)
    new_bp.append_entity(new_entity)
    return new_bp


################################################################
#
# main
if __name__ == "__main__":
    exchange_str = input_def("bp:(string or filename.txt)", "bp.txt")
    # exchange_str = """0eNrtVdFygjAQ/Jd7hg4EUeBXOo4TY6o3E5KUBK3j8O89tFKqItrX9kUGZm9vd1nMAZaqlrZC7aE4AAqjHRSvB3C41ly1z/zeSigAvSwhAM3L9k6ZNTqPIhQb6XxYyfearrKCJgDUK/kBRdwEv6YJWY+INfMApPboUZ7EHW/2C12XS1pZxOOyArDGEYHRrRYineb5SxrAHoowydlLSuu+0Is3VDRy2nT20m0gNqlCq7iXRCpM3QYXR1Fr9qy3AwtjLZkRfKkG0UmHlkoKXxndysdK1OiHZibdDF9tuRZyNTaRdhOUHNdYl6FF2xOVsh562qF3vH0bJWr6TXrkffTsBve9fLIObysjpHOo12Gth8Xn1wvWklfhbkPv4oeFeTt10Q423rZkpB/R4/0gG6iNupcuu5nuZCDd5IqaK2X2T1TjwZTTq0UDId/qybLizt0zPbtpmg2Y/q4IVzVBRzuVP/1FxNGF+CcqlTzyB3a/UvF/pf5wpehAOx6ERe/4DWBLFTjWhWXxZJazWZZl05xcNJ8RkoFp"""
    if os.path.exists(exchange_str):
        with open(exchange_str, "r") as f:
            exchange_str = f.read()

    bp = blueprint.from_string(exchange_str)
    new_bp = combine_requests_from_chests(bp)
    print(new_bp.to_str())
