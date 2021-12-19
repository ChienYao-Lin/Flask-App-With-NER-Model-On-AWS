import json
import spacy
from spacy import displacy

def lambda_handler(event, context):
    # TODO implement
    
    nlp_sm = spacy.load('/opt/python/en_core_web_sm/en_core_web_sm-3.2.0')
    nlp_skill = spacy.load('/opt/python/skill_NER')
    body = json.loads(event["body"])
    

    sentences = [str(i) for i in nlp_sm(body["text"]).sents]
    
    results = []
    for sen in sentences:
        doc = nlp_skill(sen)
        results.append(displacy.render(doc, style="ent"))
    
    return {
        'statusCode': 200,
        "body": json.dumps({
            "results": results
        })
    }
