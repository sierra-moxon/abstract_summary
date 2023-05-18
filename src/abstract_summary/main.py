"""Main python file."""
import requests


def demo():
    """Demo function."""
    print('Hello world!')


def submit_to_ars(m):
    submit_url = 'https://ars.transltr.io/ars/api/submit'
    response = requests.post(submit_url, json=m)
    try:
        message_id = response.json()['pk']
    except:
        print('fail')
        message_id = None
    print(f'https://arax.ncats.io/?source=ARS&id={message_id}')
    return message_id


def retrieve_ars_results(mid):
    message_url = f'https://ars.transltr.io/ars/api/messages/{mid}?trace=y'
    response = requests.get(message_url)
    j = response.json()
    print(j.get('status'))
    results = {}
    for child in j['children']:
        if child['status'] == 'Done':
            childmessage_id = child['message']
            child_url = f'https://ars.transltr.io/ars/api/messages/{childmessage_id}'
            child_response = requests.get(child_url).json()
            try:
                nresults = len(child_response['fields']['data']['message']['results'])
                if nresults > 0:
                    results[child['actor']['agent']] = {'message': child_response['fields']['data']['message']}
            except:
                nresults = 0
        else:
            nresults = 0
        print(child['status'], child['actor']['agent'], nresults)
    return results


if __name__ == '__main__':
    qg = {
        "nodes": {
            "n0": {
                "name": "Glycerol",
                "id": "PUBCHEM.COMPOUND:753"
            },
            "n1": {
                "category": [
                    "biolink:BiologicalProcessOrActivity"
                ],
                "name": "Biological Process Or Activity"
            },
            "n2": {
                "id": "NCBIGene:2710"
            }
        },
        "edges": {
            "e0": {
                "subject": "n0",
                "object": "n1",
                "predicate": [
                    "biolink:related_to"
                ]
            },
            "e1": {
                "subject": "n1",
                "object": "n2",
                "predicate": [
                    "biolink:related_to"
                ]
            }
        }
    }

    process_query = {'message': {'query_graph': qg}}
    glycerol_process_id = submit_to_ars(process_query)
    results = retrieve_ars_results(glycerol_process_id)
    print(results.get('ara-arax'))
