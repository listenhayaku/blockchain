
def miner(appendix):

    if("miner:" in appendix):
        print("[appendix.miner]miner is is appendix")
        appendix = appendix.split("\\")
        for _ in appendix:
            if("miner:" in _):
                appendix = _.split("miner:")[1]
                break
        print("[appendix.miner]appendix = ",appendix)
        return appendix
    else:
        print("[appendix.miner]miner is not in appendix")

if __name__ == "__main__":
    print("this is program is not for running directly")