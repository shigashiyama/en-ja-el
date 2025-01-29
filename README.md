# EnJaEL: En-Ja Parallel Entity Linking Dataset (Version 1.0)

## Overview

This dataset was constructed by translating original English texts in existing English entity linking datasets (VoxEL, MEANTIME, and Linked-DocRed) to Japanese while preserving annotation information.
This includes mention spans for named entity recognition and knowledge base entry IDs for entity disabiguation.
The texts were machine translated using the model from [Min'na no Jidou Hon'yaku@TexTra](https://mt-auto-minhon-mlt.ucri.jgn-x.jp/) and then fully post-edited by human translators.
We added links to Wikidata entities and Wikipedia pages based on intra-KB links when the original datasets did not include them. 
For example, the original MENATIME data only contained DBpedia links, so we added Wikidata  and Wikipedia links.

## Data Statistics

The data statistics are as follows. 

You can confirm them using the following commmand (with Python 3.8.0 or later). For example,
- `python3 src/show_data_statistics.py -i data/json_split/train.json`

|			     |VoxEL|MEANTIME|Linked-DocRed|
|--			     |--:  | --:    |--:          |
|Document		     |	 15|	 120|          500|
|Sentence		     |	 94|   1,797|	     3,944|
|Mention		     |	204|   2,634|	    12,897|
|Mention w/ Wikidata link    |	201|   1,861|	     9,446|
|Mention w/ Wikipedia_En link|	201|   1,867|	     9,535|
|Mention w/ Wikipedia_Ja link|	187|   1,781|	     6,127|
|Mention w/ DBpedia link     |	   |   1,871|		  |
|Entity			     |	204|   1,407|	     9,779|
|Entity w/ Wikidata link     |	201|	 785|	     6,607|
|Entity w/ Wikipedia_En link |	201|	 789|	     6,690|
|Entity w/ Wikipedia_Ja link |	187|	 747|	     4,410|
|Entity w/ DBpedia link	     |	   |	 791|		  |

The number of mentions for each entity type is as follows.
For Linked-DocRed, the names of living persons are masked with `■` symbols, and their spans are annotated with the `PER_MASKED` type.

|Type      |VoxEL|MEANTIME|Linked-DocRed|
|--	   |--:	 |--:     |--:          |
|No_Label  |  204|   2,634|             |
|PER	   |     |        |        1,260|
|PER_MASKED|	 |	  |        1,088|
|LOC	   |     |        |        4,122|
|ORG	   |     |        |        1,838|
|NUM	   |	 |	  |          669|
|TIME	   |	 |	  |        1,996|
|MISC	   |	 |	  |        1,924|

## Data Format

### JSON

- A document object value is assosiated with a key that represents the
  document ID (e.g., 001-1). Each document object has the sets of
  `doc_info`, `sentences`, `mentions`, and `entities`.
    ~~~~
    "001": {
      "doc_info": {
        "title": null,
        "url": "http://www.voxeurop.eu/en/2017/social-issues-5121271"
      },
      "sentences": {
      ...
      },
      "mentions": {
      ...
      },
      "entities": {
      ...
      }
    }
    ~~~~
- A sentence object under `sentences` is as follows
    ~~~~
    "sentences": {
      "00": {
        "text": "EUの失業率は2008年以来の最低水準。",
        "mention_ids": [
          "M001"
        ]
      },
      ...
    },
    ~~~~
- A mention object under `mentions` is as follows:
    ~~~~
    "mentions": {
      "M001": {
        "sentence_id": "00",
        "span": [
          0,
          2
        ],
        "text": "EU",
        "entity_type": null,
        "entity_id": "E001"
      },
      ...
    },
    ~~~~
- An entity object, which corresponds to a set of one or more mentions,
  under `entities` is as follows.  
    ~~~~
    "entities": {
      "E001": {
        "member_mention_ids": [
          "M001"
        ],
        "entity_type": null,
        "has_enwiki_ref": true,
        "has_jawiki_ref": true,
        "has_wikidata_ref": true,
        "has_dbpedia_ref": false,
        "ref_urls": {
          "en.wikipedia": "https://en.wikipedia.org/wiki/European_Union",
          "wikidata": "http://www.wikidata.org/entity/Q458",
          "ja.wikipedia": "https://ja.wikipedia.org/wiki/%E6%AC%A7%E5%B7%9E%E9%80%A3%E5%90%88"
        }
      },
      ...
    }
    ~~~~

## Data Sources and License

- The VoxEL data
  - We used `sVoxEL-en.ttl` from the [VoxEL benchmark dataset](https://users.dcc.uchile.cl/~hrosales/VoxEL.html).
  - Our extended data is licensed under [Academic Research Non-Commercial Limited CC-BY-NC-SA Reference-Type License](https://github.com/shigashiyama/en-ja-el/LICENSE_ARNC-Limited-CC-BY-NC-SA).
)
- The MEANTIME data
  - We used 120 documents in `intra_cross-doc_annotation` from the NewsReader [MEANTIME corpus](http://www.newsreader-project.eu/results/data/wikinews/) (`meantime_newsreader_english_oct15.zip`).
  - Our extended data is licensed under [Academic Research Non-Commercial Limited CC-BY-NC-SA Reference-Type License](https://github.com/shigashiyama/en-ja-el/LICENSE_ARNC_CC_RT.md).
- The Linked-DocRED data
  - We used `test_revised.json` from [Linked-Re-DocRED](https://github.com/alteca/Linked-DocRED/tree/main/Linked-Re-DocRED).
  - Our extended data is licensed under the [GPLv3 License](https://github.com/shigashiyama/en-ja-el/LICENSE_ARNC_CC_RT.md).
    ~~~~
    EnJaEL Linked-DocRED
    Copyright (C) 2025 National Institute of Information and Communications Technology (Shohei Higashiyama)
     
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.
     
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.
     
    You should have received a copy of the GNU General Public
    License along with this program. If not, see <http://www.gnu.org/licenses/>.
    ~~~~

## Change Log

- 2025/01/29: The Version 1.0 has been released.

## Citation

Please cite the following paper.

Japanese bibliography:
~~~~
@article{higashiyama-etal-2024-cadel,
    author  = "東山,翔平 and 出内,将夫 and 内山,将夫",
    title   = "日本語エンティティリンキングのための行政機関ウェブ文書コーパスの構築",
    journal = "情報処理学会研究報告",
    volume  = "2024-NL-260",
    number  = "10",
    pages   = "1--15",   
    year    = "2024",
    month   = "jun"
    url     = "https://ipsj.ixsq.nii.ac.jp/ej/index.php?active_action=repository_view_main_item_detail&page_id=13&block_id=8&item_id=235101&item_no=1",
}
~~~~

English bibliography:
~~~~
@article{higashiyama-etal-2024-cadel,
    author  = "Shohei Higashiyama and Masao Ideuchi and Masao Utiyama",
    title   = "Construction of the Administrative Agency Web Document Corpus for {Japanese} Entity Linking [in {Japanese}]",
    journal = "IPSJ SIG Technical Report",
    volume  = "2024-NL-260",
    number  = "10",
    pages   = "1--15",   
    year    = "2024",
    month   = "jun",
    url     = "https://ipsj.ixsq.nii.ac.jp/ej/index.php?active_action=repository_view_main_item_detail&page_id=13&block_id=8&item_id=235101&item_no=1",
}
~~~~

## Reference

VoxEL
MEANTIME

[1] Tan, Qingyu, Lu Xu, Lidong Bing, Hwee Tou Ng, and Sharifah Mahani Aljunied. Revisiting DocRED - Addressing the False Negative Problem in Relation Extraction. In Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing, 8472–87. Abu Dhabi, United Arab Emirates: Association for Computational Linguistics, 2022. https://aclanthology.org/2022.emnlp-main.580.
