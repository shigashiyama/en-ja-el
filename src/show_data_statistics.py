import argparse
from collections import Counter
import json
import sys


def load_json(
        input_path: str,
) -> dict:

    with open(input_path, encoding='utf-8') as f:
        print(f'Read: {input_path}', file=sys.stderr)
        data = json.load(f)
    return data


def write_as_json(
        data: dict,
        output_path: str,
) -> None:

    with open(output_path, 'w', encoding='utf-8') as fw:
        json.dump(data, fw, ensure_ascii=False, indent=2)
    print(f'Saved: {output_path}', file=sys.stderr)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input_json_paths', '-i',
        type=str,
        required=True,
    )
    parser.add_argument(
        '--reference_json_paths', '-r',
        type=str,
    )
    args = parser.parse_args()

    data = {}
    for input_path in args.input_json_paths.split(','):
        data_tmp = load_json(input_path)
        data.update(data_tmp)

    ref_data = {}
    if args.reference_json_paths:
        for ref_path in args.reference_json_paths.split(','):
            data_tmp = load_json(ref_path)
            ref_data.update(data_tmp)
    
    # show statistics
    counter = Counter()
    key2sets = {'num_mens': set()}

    for doc_id, doc in data.items():
        counter['num_docs'] += 1

        if 'sentences' in doc:
            counter['num_sens'] += len(doc['sentences'])

        if 'mentions' in doc:
            counter['num_mens'] += len(doc['mentions'])

            for men_id, men in doc['mentions'].items():
                key2sets['num_mens'].add(men['text'])

                if 'entity_type' in men:
                    key = f'num_mens:{men["entity_type"]}'
                    counter[key] += 1
                    if not key in key2sets:
                        key2sets[key] = set()
                    key2sets[key].add(men['text'])

                if men['entity_id'] == None:
                    continue
                    
                ent = doc['entities'][men['entity_id']]
                if 'has_wikidata_ref' in ent and ent['has_wikidata_ref']:
                    counter['num_mens:has_wd_ref'] += 1
                if 'has_jawiki_ref' in ent and ent['has_jawiki_ref']:
                    counter['num_mens:has_jawiki_ref'] += 1
                if 'has_enwiki_ref' in ent and ent['has_enwiki_ref']:
                    counter['num_mens:has_enwiki_ref'] += 1
                if 'has_dbpedia_ref' in ent and ent['has_dbpedia_ref']:
                    counter['num_mens:has_dp_ref'] += 1

        if 'entities' in doc:
            counter['num_ents'] += len(doc['entities'])

            for ent_id, ent in doc['entities'].items():
                if 'has_wikidata_ref' in ent and ent['has_wikidata_ref']:
                    counter['num_ents:has_wd_ref'] += 1
                if 'has_jawiki_ref' in ent and ent['has_jawiki_ref']:
                    counter['num_ents:has_jawiki_ref'] += 1
                if 'has_enwiki_ref' in ent and ent['has_enwiki_ref']:
                    counter['num_ents:has_enwiki_ref'] += 1
                if 'has_dbpedia_ref' in ent and ent['has_dbpedia_ref']:
                    counter['num_ents:has_dbpedia_ref'] += 1

    print('\n#Data statistics.\n#key\ttotal\t(unique)')
    main_keys = ['num_docs', 'num_sens', 'num_mens', 'num_ents']
    for key in main_keys:
        val = counter[key]
        if key in key2sets:
            val2 = len(key2sets[key])
            print(f'{key}\t{val}\t({val2})')
        else:
            print(f'{key}\t{val}')
        
    for key, val in sorted(counter.items()):
        if not key in main_keys:
            if key in key2sets:
                val2 = len(key2sets[key])
                print(f'{key}\t{val}\t({val2})')
            else:
                print(f'{key}\t{val}')

    if ref_data:        
        ref_mention_wd_set = set()
        ref_mention_jw_set = set()
        ref_mention_ew_set = set()
        ref_mention_dbpedia_set = set()

        mention_wd_all = mention_wd_known = 0
        mention_jw_all = mention_jw_known = 0
        mention_ew_all = mention_ew_known = 0
        mention_dbpedia_all = mention_dbpedia_known = 0

        for subdoc_id, doc in ref_data.items():
            for men_id, men in doc['mentions'].items():
                men_text = men['text']
                ent = doc['entities'][men['entity_id']]
                
                if ent['has_wikidata_ref']:
                    wd_url = ent['ref_urls']['wikidata']
                    ref_mention_wd_set.add((men_text, wd_url))
             
                if ent['has_jawiki_ref']:
                    jw_url = ent['ref_urls']['ja.wikipedia']
                    ref_mention_jw_set.add((men_text, jw_url))
             
                if ent['has_enwiki_ref']:
                    wp_url = ent['ref_urls']['en.wikipedia']
                    ref_mention_wp_set.add((men_text, ew_url))
             
                if ent['has_dbpedia_ref']:
                    dbpedia_url = ent['ref_urls']['dbpedia']
                    ref_mention_dbpedia_set.add((men_text, dbpedia_url))

        for subdoc_id, doc in data.items():
            for men_id, men in doc['mentions'].items():
                men_text = men['text']
                ent = doc['entities'][men['entity_id']]
                
                if ent['has_wikidata_ref']:
                    wd_url = ent['ref_urls']['wikidata']
                    key = (men_text, wd_url)
                    mention_wd_all += 1
                    if key in ref_mention_wd_set:
                        mention_wd_known += 1
             
                if ent['has_jawiki_ref']:
                    jw_url = ent['ref_urls']['ja.wikipedia']
                    key = (men_text, jw_url)
                    mention_jw_all += 1
                    if key in ref_mention_jw_set:
                        mention_jw_known += 1
             
                if ent['has_enwiki_ref']:
                    ew_url = ent['ref_urls']['en.wikipedia']
                    key = (men_text, ew_url)
                    mention_ew_all += 1
                    if key in ref_mention_ew_set:
                        mention_ew_known += 1
             
                if ent['has_dbpedia_ref']:
                    dbpedia_url = ent['ref_urls']['openstreetmap']
                    key = (men_text, dbpedia_url)
                    mention_dbpedia_all += 1
                    if key in ref_mention_dbpedia_set:
                        mention_dbpedia_known += 1
                           
        print('\n#Instance statistics. (instance: a pair of a mention text and its link)')
        print('#num_all_ins\tratio_unknown_ins')
        print(f'WD:\t{mention_wd_all}\t{(mention_wd_all-mention_wd_known)/mention_wd_all:.2f}')
        print(f'JWP:\t{mention_jw_all}\t{(mention_jw_all-mention_jw_known)/mention_jw_all:.2f}')
        print(f'EWP:\t{mention_ew_all}\t{(mention_ew_all-mention_ew_known)/mention_ew_all:.2f}')
        print(f'DBP:\t{mention_dbpedia_all}\t{(mention_dbpedia_all-mention_dbpedia_known)/mention_dbpedia_all:.2f}')


if __name__ == '__main__':
    main()
