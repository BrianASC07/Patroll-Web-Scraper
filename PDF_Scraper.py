import pdfplumber
import os
import json
import re
from collections import defaultdict

LEFT_COL_X_LIMIT = 250  # Adjust depending on actual PDF layout
def extract_patent_id(text):
    patent_id_match = re.search(r'U\.S\. Patent No\. (\d{1,3},\d{3}(?:,\d{3})?)', text)
    if patent_id_match:
        raw_id = patent_id_match.group(1)
        patent_id = "US" + raw_id.replace(",", "")
    else:
        patent_id = "Not found"
    return patent_id
def parse_pdf_by_layout(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_features = {}
        current_feature = None
        description_lines = []
        feature_quotes = defaultdict(list)
        patent_id = extract_patent_id(pdf.pages[0].extract_text())
        for page in pdf.pages:
            words = page.extract_words()
            # Group into left and right columns
            left_col = []
            right_col = []
            for w in words:
                x0 = float(w['x0'])
                if x0 < LEFT_COL_X_LIMIT:
                    left_col.append(w)
                else:
                    right_col.append(w)
            # Merge lines by top coordinate for left and right
            left_lines = group_by_line(left_col)
            right_lines = group_by_line(right_col)
            for line in left_lines:
                text = line['text']
                feature_match = re.match(r'^(\d{1,2}(?:\.[a-z])?)\.\s+(.*)', text)
                if feature_match:
                    # Save previous feature
                    if current_feature:
                        all_features[current_feature] = {
                            "Description": ' '.join(description_lines).strip(),
                            "Feature_Quotes": dict(feature_quotes)
                        }
                    # Start new feature
                    current_feature = feature_match.group(1)
                    description_lines = [feature_match.group(2)]
                    feature_quotes = defaultdict(list)
                else:
                    # Continue description
                    if current_feature:
                        description_lines.append(text)
            for line in right_lines:
                text = line['text']
                quote_match = re.match(r'^([ABC])\.?\s*(US\d{7})?:?\s*(.*)', text)
                if quote_match:
                    label, pid, quote = quote_match.groups()
                    pid = pid or get_patent_id_from_label(label)
                    feature_quotes[pid].append(quote.strip())
                elif current_feature and feature_quotes:
                    # Likely a continuation of the last quote
                    last_pid = list(feature_quotes.keys())[-1]
                    feature_quotes[last_pid].append(text.strip())
        # Save final feature
        if current_feature:
            all_features[current_feature] = {
                "Description": ' '.join(description_lines).strip(),
                "Feature_Quotes": dict(feature_quotes)
            }
    return {
        "Patent_ID": patent_id,
        "Features": all_features
    }
def group_by_line(words, y_tolerance=3):
    """Group words into lines based on 'top' position"""
    lines = []
    words.sort(key=lambda w: (round(w['top'], 1), w['x0']))
    line_map = defaultdict(list)
    for w in words:
        key = round(w['top'] / y_tolerance)
        line_map[key].append(w)
    for line_words in sorted(line_map.values(), key=lambda lw: lw[0]['top']):
        line_text = ' '.join(w['text'] for w in line_words)
        lines.append({
            'top': line_words[0]['top'],
            'text': line_text
        })
    return lines
def get_patent_id_from_label(label):
    return {
        'A': 'US6704281',
        'B': 'US20090185619',
        'C': 'US8428148'
    }.get(label, f'Unknown_{label}')
# Example usage
pdf_path = "PATROLL_OptiMorphix_US8621061.pdf"
result = parse_pdf_by_layout(pdf_path)
with open("parsed_output.json", "w") as f:
    json.dump(result, f, indent=2)
print(":white_check_mark: Parsing complete. Output saved to parsed_output.json")

