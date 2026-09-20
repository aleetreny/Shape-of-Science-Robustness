"""Prepare writing indices from saved results; never run scientific calculations."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def read(path):
    return json.loads((ROOT / path).read_text())


def write_csv(name, rows):
    with (HERE / name).open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    # Main table 2: exact frozen configuration, including the adapter revision.
    citations = {
        "specter": "cohan-etal-2020-specter",
        "specter2": "singh-etal-2023-scirepeval",
        "scincl": "ostendorff-etal-2022-neighborhood",
        "scibert": "beltagy-etal-2019-scibert",
        "bert": "devlin-etal-2019-bert",
        "mpnet": "reimers-gurevych-2019-sentence; exact checkpoint model card",
        "minilm": "reimers-gurevych-2019-sentence; exact checkpoint model card",
        "pubmedbert": "reff9ebfb9307",
        "biobert": "ref4f3e28932e",
        "simcse": "gao-etal-2021-simcse",
    }
    models = []
    for m in read("config/embeddings_v1.json")["models"]:
        models.append(dict(
            model=m["key"], display_name=m["name"], repo_id=m["repo_id"],
            revision=m["revision"], adapter_repo=m.get("adapter", {}).get("repo_id", ""),
            adapter_revision=m.get("adapter", {}).get("revision", ""),
            dimension=m["dimension"], native_max_tokens=m["max_length"],
            primary_pooling="mean" if m["key"] in {"scibert", "bert", "pubmedbert", "biobert"} else m["poolings"][0],
            text_format=m["text_format"], native_input="title + abstract",
            reference=citations[m["key"]], model_card="https://huggingface.co/" + m["repo_id"],
            source="config/embeddings_v1.json; POOLING.md"))
    write_csv("table2_models.csv", models)
    panels = [
        ("Original corpus", "500000 IDs: 400000 base + 100000 supplement", "Ten models; title + abstract", "26 Fields x five periods; global summaries use the base", "Fixed eligible OpenAlex corpus; not world-proportional", "CORPUS_PROTOCOL.md; METHODS_ANALYSIS.md"),
        ("Three text inputs", "52000 IDs: 400 per Field-period; 2000 per Field", "Ten models; title / abstract / both", "Same IDs and candidate sets within each Field", "Includes 26000 pilot IDs; not three inputs over 500000", "METHODS_ROBUSTNESS.md"),
        ("Common text fragment", "A different 52000-ID selection: 400 per cell", "Native versus shared content fragment", "Paired IDs and content characters; model-specific tokenizers", "Different panel from three inputs; panels may overlap", "METHODS_ANALYSIS.md"),
        ("Matched group size", "256 articles per centre; 26 Fields / 217 Subfields / 26 Subfield centres", "Ten models; native input", "Within-group comparison: 26 Fields and same 183 Subfields at 128/256/512", "Centres and within-group structures are different objects", "METHODS_ROBUSTNESS.md"),
        ("Paired Field/Subfield searches", "217 Subfields x 50 queries = 10850 queries; ten selections", "Ten models; native input; k25 primary", "256 candidates per scope, including all 50 query articles", "Field scope is conditioned on those queries; self excluded during search", "METHODS_ROBUSTNESS.md"),
        ("Geometry and field pairs", "2000 per Field; twenty halves of 1000; five selections of 2000", "Ten models; two primary properties; 325 field pairs", "26 saved selection conditions per model and field pair", "Same fixed corpus; alternatives and point controls have different coverage", "METHODS_MORPHOLOGY.md; METHODS_FIELD_PAIRS.md"),
    ]
    write_csv("table1_panels.csv", [dict(zip(
        ["panel", "size", "representation", "comparison", "limit", "source"], row)) for row in panels])

    # Paragraph allocations are an editorial plan, not a fixed syntactic template.
    sections = {
        "1": ("Introduction", [("I1", 170), ("I2", 210), ("I3", 210), ("I4", 210)]),
        "2": ("Background and research questions", [("B11", 140), ("B12", 110), ("B21", 160), ("B22", 120), ("B31", 130), ("B32", 90)]),
        "3": ("Data and comparative design", [("M11", 180), ("M12", 180), ("M21", 140), ("M22", 130), ("M31", 230), ("M32", 230), ("M41", 170), ("M42", 170), ("M51", 100), ("M52", 70)]),
        "4": ("Results", [("R11", 100), ("R12", 120), ("R13", 140), ("R14", 90), ("R21", 120), ("R22", 130), ("R23", 140), ("R24", 110), ("R31", 100), ("R32", 150), ("R33", 150), ("R34", 100), ("R41", 130), ("R42", 140), ("R43", 140), ("R44", 140), ("R45", 170), ("R46", 80)]),
        "5": ("Discussion", [("D11", 140), ("D12", 110), ("D21", 150), ("D22", 130), ("D31", 130), ("D32", 90), ("D41", 150), ("D42", 160), ("D43", 90)]),
        "6": ("Conclusion", [("C1", 200)]),
    }
    paras = [dict(section=k, section_title=title, paragraph=pid, planned_words=n)
             for k, (title, ps) in sections.items() for pid, n in ps]
    assert len(paras) == 48 and sum(x["planned_words"] for x in paras) == 6750
    write_csv("paragraph_plan.csv", paras)

    main_items = [
        ("Table 1", "Corpus and analytical panels", "M12", "research/writing_blueprint_2026-09-18/table1_panels.csv", "Prepared content; journal typesetting pending"),
        ("Table 2", "Embedding models and primary representation settings", "M21", "research/writing_blueprint_2026-09-18/table2_models.csv", "Prepared content; full hashes in supplementary table"),
        ("Figure 1", "Agreement between group centres and within groups", "R12", "reports/robustness_v2/final/figures/02_scales.pdf", "Existing figure; final numbering and caption pending"),
        ("Figure 2", "Neighbour agreement in matched Field and Subfield searches", "R22", "reports/robustness_v2/final/figures/03_paired_neighbors.pdf", "Existing figure; final numbering and caption pending"),
        ("Figure 3", "Changes associated with the encoder and text input", "R32", "reports/robustness_v2/final/figures/01_input_effect.pdf", "Existing figure; final numbering and caption pending"),
        ("Figure 4", "Persistence, reversal and magnitude of field comparisons", "R42", "reports/field_pair_summary_v1/01_conclusions_and_magnitude.pdf", "Existing figure; Spanish labels require English presentation copy"),
    ]
    supplements = [
        ("Figure S1", "Input stability alerts", "S3.4", "reports/robustness_v2/final/figures/07_input_alerts.pdf"),
        ("Figure S2", "Subfield persistence", "S4.3", "reports/prepaper_v1/figures/01_subfield_persistence.pdf"),
        ("Figure S3", "Dependence of specific relations", "S4.3", "reports/prepaper_v1/figures/02_relation_dependence.pdf"),
        ("Figure S4", "Time and candidate controls", "S5.1", "reports/robustness_v2/final/figures/04_time_controls.pdf"),
        ("Figure S5", "Medicine and composition", "S5.2", "reports/robustness_v2/final/figures/05_medicine_composition.pdf"),
        ("Figure S6", "Pooling and model families", "S5.3", "reports/robustness_v2/final/figures/06_recipe_families.pdf"),
        ("Figure S7", "Sample size and geometric properties", "S6.2", "reports/morphology_pilot_v1/03_sample_size.pdf"),
        ("Figure S8", "Control rank agreement", "S6.3", "reports/morphology_pilot_v1/05_control_rank_agreement.pdf"),
        ("Figure S9", "Counterexamples to fragmentation", "S6.4", "reports/morphology_pilot_v1/04_fragmentation_counterexamples.pdf"),
        ("Figure S10", "All field-pair comparisons", "S7.1", "reports/field_pair_summary_v1/02_all_field_pairs.pdf"),
    ]
    displays = [dict(item=n, title=t, after_paragraph=p, source=f, status=s, scope="main") for n, t, p, f, s in main_items]
    displays += [dict(item=n, title=t, after_paragraph=p, source=f, status="Existing base; supplementary layout not yet produced", scope="supplement") for n, t, p, f in supplements]
    assert all((ROOT / row["source"]).exists() for row in displays)
    write_csv("display_items.csv", displays)

    # Copy selected cells/JSON values with explicit selectors, without recomputing science.
    claims = []

    def csv_claim(cid, para, source, selector, columns, displayed, limit):
        rows = list(csv.DictReader((ROOT / source).open()))
        selected = [r for r in rows if all(r[k] == str(v) for k, v in selector.items())]
        assert len(selected) == 1, (cid, len(selected))
        claims.append(dict(claim_id=cid, paragraph=para, source=source,
                           source_sha256=hashlib.sha256((ROOT / source).read_bytes()).hexdigest(),
                           selector=json.dumps(selector, sort_keys=True), json_pointer="",
                           values=json.dumps({k: selected[0][k] for k in columns}, sort_keys=True),
                           displayed=displayed, limit=limit))

    def json_claim(cid, para, source, pointer, displayed, limit):
        value = read(source)
        for part in pointer.split("/"):
            value = value[int(part)] if isinstance(value, list) else value[part]
        claims.append(dict(claim_id=cid, paragraph=para, source=source,
                           source_sha256=hashlib.sha256((ROOT / source).read_bytes()).hexdigest(),
                           selector="", json_pointer=pointer, values=json.dumps(value, sort_keys=True),
                           displayed=displayed, limit=limit))

    original = "reports/analysis_v1/final/summary.json"
    json_claim("E01", "R21", original, "neighbors/25/cell_pair_overlap/mean", "30.3%", "Balanced cell-pair average; full within-cell candidate universes")
    json_claim("E02", "R21", original, "equal_neighbors/mean/25/mean", "31.9%", "2048 candidates per cell; not the 256 paired-scope experiment")
    structural = "reports/robustness_v2/final/tables/structure_paired_scope_summary.csv"
    csv_claim("E03", "R22", structural, {"k": "25"}, ["subfields", "subfields_lower_agreement", "subfields_higher_agreement", "mean_difference"], "127 lower / 90 higher of 217; -1.35 percentage points", "Same 50 queries included in each 256 candidate set; ten selections")
    csv_claim("E04", "R23", structural, {"k": "50"}, ["subfields", "subfields_lower_agreement", "subfields_higher_agreement"], "109 lower / 108 higher of 217", "Sensitivity to k; not an independent sample")
    inputs = "reports/robustness_v2/final/tables/input_input_effect_summary.csv"
    for i, (metric, condition, measure, display) in enumerate([
        ("neighbors25", "title", "model_change_at_full", "68.76%"),
        ("neighbors25", "title", "input_change_from_full", "70.67%"),
        ("neighbors25", "abstract", "input_change_from_full", "22.12%"),
        ("cka", "title", "model_change_at_full", "0.3700"),
        ("cka", "title", "input_change_from_full", "0.3658"),
        ("cka", "abstract", "input_change_from_full", "0.0269"),
    ], 5):
        csv_claim(f"E{i:02}", "R32", inputs, dict(metric=metric, input_condition=condition, measure=measure), ["n", "mean"], display, "52000 shared IDs; 260 model-Field cases; mean recipe; close averages are not equivalence")
    json_claim("E11", "R34", "reports/robustness_v2/final/summary.json", "input/alert_counts/2", "72/520 to 5/520; 100 selections", "Shape contrast stability; not all neighbours/recipes or population confidence")
    pairs = "reports/field_pair_summary_v1/classification_summary.csv"
    for metric, counts in [("angle_p50", (42, 262, 21)), ("pr", (54, 221, 50))]:
        csv_claim("E12" if metric == "angle_p50" else "E13", "R42", pairs, dict(metric=metric, rule="all_saved", minimum_relative_difference="0.0"), ["unanimous", "contradiction", "unresolved", "pairs", "observations_per_model_pair"], "/".join(map(str, counts)) + " of 325", "26 selection conditions; two persistent opposite models suffice for contradiction")
    for cid, metric, threshold, display in [("E14", "angle_p50", "0.05", "96/325"), ("E15", "pr", "0.05", "177/325"), ("E16", "angle_p50", "0.1", "19/325"), ("E17", "pr", "0.1", "126/325")]:
        csv_claim(cid, "R43", pairs, dict(metric=metric, rule="all_saved", minimum_relative_difference=threshold), ["unanimous", "contradiction", "unresolved", "pairs"], display, "Operational symmetric relative minimum, not significance or universal relevance")
    panels_source = "reports/field_pair_summary_v1/model_panel_summary.csv"
    for cid, metric, panel, column, display in [("E18", "angle_p50", "all_ten", "contradiction_and_alternatives", "225/325"), ("E19", "pr", "all_ten", "contradiction_and_alternatives", "196/325"), ("E20", "angle_p50", "six_similarity", "contradiction", "231/325"), ("E21", "pr", "six_similarity", "contradiction", "160/325")]:
        csv_claim(cid, "R44", panels_source, dict(metric=metric, panel=panel, minimum_relative_difference="0.0"), [column, "pairs", "models"], display, "Same witnesses under alternatives; angle 26 conditions, spectrum three; six-model panel has fewer opportunities for opposition")
    controls = "reports/field_pair_summary_v1/control_summary.csv"
    for cid, metric, display in [("E22", "angle_p50", "145/262"), ("E23", "pr", "218/221")]:
        csv_claim(cid, "R45", controls, dict(metric=metric, condition="global_centered", minimum_relative_difference="0.0"), ["same_original_witness_pair_retained", "original_persistent_contradictions"], display, "Point control: same original opposite witness identities and signs retained in reference and variant")
    write_csv("claim_evidence.csv", claims)
    (HERE / "claim_evidence.json").write_text(json.dumps(claims, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(dict(models=len(models), panels=len(panels), paragraphs=len(paras), words=6750, main_items=6, supplementary_figure_bases=10, claim_rows=len(claims))))


if __name__ == "__main__":
    main()
