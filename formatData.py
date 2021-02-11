import json
import os
import datetime
import traceback


def main():
    pageNum = 0
    outS = ""

    path = os.path.abspath(
        os.path.join(
            os.getcwd(),
            "data.json"
        )
    )

    with open(path) as f:
        payload = json.load(f)

    for item in payload:
        create = {'create': {
            "_index": "recipes",
            "_type": "rwebdoc",
            "_id": str(pageNum)
        }}
        out = {
            "id": str(pageNum),
            "recipeLink": item["recipeLink"],
            "recipeTitle": item["recipeTitle"],
            "specialEquipment": item["specialEquipment"],
            "notes": item["notes"],
            "activeTime": item["activeTime"],
            "totalTime": item["totalTime"],
            "direction": item["direction"],
            "ingredients": item["ingredients"]
        }
        outS += json.dumps(create, indent=4) + "\n" + json.dumps(out, indent=4) + "\n"
        pageNum += 1

    ofname = os.path.abspath(
        os.path.join(
            os.getcwd(),
            "ofile.txt"
        )
    )
    of = open(ofname, 'w')
    of.write(outS)
    of.close()
    return


if __name__ == "__main__":
    pStart = datetime.datetime.now()
    try:
        main()
    except Exception as errorMain:
        print("Fail End Process: {0}".format(errorMain))
        traceback.print_exc()
    qStop = datetime.datetime.now()
    print("Execution time: " + str(qStop - pStart))
