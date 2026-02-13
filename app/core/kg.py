from gliner2 import GLiNER2
from loguru import logger
from app.schemas.kg import KG_triple, KG_triples

def extract_kg_triples_from_gliner2_entities(paper_title: str, entities_list: list):
    """Extract knowledge graph triples from GLiNER2 entities."""
    kg_triples : KG_triples = KG_triples(triples=[])
    for entity in entities_list:
        tasks = entity.get("task", None)
        methods = entity.get("method", None)
        metrics = entity.get("metric", None)
        datasets = entity.get("dataset", None)
        concepts = entity.get("concept", None)
        
        if concepts:    
            kg_triples.triples.append(KG_triple(paper_title, "CITE", c) for c in concepts)
        if tasks:
            kg_triples.triples.append((paper_title, "TREAT", t) for t in tasks)
        if datasets:
            kg_triples.triples.append((paper_title, "USE", d) for d in datasets)
        if methods:
            kg_triples.triples.append((paper_title, "USE", m) for m in methods)
        if metrics:
            kg_triples.triples.append((paper_title, "USE", m) for m in metrics)
    
    return kg_triples
    
def construct_KG_from_articles_list(articles_list:list):

    extractor = GLiNER2.from_pretrained("fastino/gliner2-base-v1")
    
    ent_structure = {
        "task": "Research task or objective (e.g., text classification, NL2SQL, machine translation)",
        "method": "Algorithm, model, or technique proposed or used (e.g., Transformer, CRF, fine-tuning)",
        "dataset": "Datasets or benchmarks used for evaluation (e.g., SQuAD, ImageNet, Spider)",
        "metric": "Evaluation metrics or scores reported (e.g., F1, BLEU, accuracy)",
        "concept": "General CS/NLP concepts mentioned in the text that do not fit the other categories (e.g., embeddings, knowledge graphs, attention mechanism)"
    }
    kg_triples : KG_triples = KG_triples(triples=[])
    for r in articles_list:
        entities = extractor.extract_entities(
        r.title+" "+r.summary,
        ent_structure
    )
        kg_triples.triples.extend(extract_kg_triples_from_gliner2_entities(r.title, entities))
        print("###############")
        logger.debug(entities)
        logger.debug(kg_triples)
        
    return kg_triples