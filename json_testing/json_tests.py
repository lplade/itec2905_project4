import json

with open('sample.json') as json_data:
    d = json.load(json_data)

    print("Retrieved {} items".format(d['total_items']))
    # print(json.dumps(d, indent=4, sort_keys=True))

    raw_event_list = d['events']['event']

    for event in raw_event_list:
        print("EVENT!!!")
        #print(json.dumps(event, indent=4, sort_keys=True))
        print(event['title'])
