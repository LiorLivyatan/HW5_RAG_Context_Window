# Data Directory - Context Windows Lab

## Overview

This directory contains all data used in the Context Windows Lab experiments. The data is organized to support reproducible, transparent experimentation with Large Language Models and Retrieval-Augmented Generation (RAG).

## Directory Structure

```
data/
├── raw/                          # Source data (manually created or collected)
│   └── hebrew_documents/         # Hebrew documents for Experiment 3
│       ├── technology/           # 7 technology documents
│       ├── law/                  # 7 law documents
│       ├── medicine/             # 6 medicine documents
│       └── metadata.json         # Document metadata
├── synthetic/                    # Auto-generated synthetic data (cached)
│   └── .gitkeep
└── README.md                     # This file
```

---

## Raw Data

### Hebrew Documents (`raw/hebrew_documents/`)

**Purpose**: Real document corpus for **Experiment 3: RAG Impact**

**Assignment Requirement** (from context-windows-lab.pdf):
> מאגר של 20 מסמכים בעברית (נושאים: טכנולוגיה, משפט, רפואה)
>
> "A repository of 20 documents in Hebrew (topics: technology, law, medicine)"

**Specifications**:
- **Total**: 20 documents
- **Language**: Hebrew (עברית)
- **Length**: 500-700 words each
- **Format**: Plain text (.txt files, UTF-8 encoding)
- **Domains**:
  - Technology (טכנולוגיה): 7 documents
  - Law (משפט): 7 documents
  - Medicine (רפואה): 6 documents

**Document List**:

#### Technology Domain (7 documents)
1. `ai_machine_learning.txt` - Artificial Intelligence and Machine Learning
2. `cybersecurity.txt` - Cybersecurity and Data Protection
3. `cloud_computing.txt` - Cloud Computing and Infrastructure
4. `iot.txt` - Internet of Things (IoT)
5. `blockchain.txt` - Blockchain and Cryptocurrencies
6. `software_dev.txt` - Software Development Methodologies
7. `mobile_apps.txt` - Mobile Applications and Development

#### Law Domain (7 documents)
1. `contract_law.txt` - Contract Law Fundamentals
2. `intellectual_property.txt` - Intellectual Property Rights
3. `privacy_law.txt` - Privacy and Data Protection Law
4. `employment_law.txt` - Employment Law
5. `corporate_law.txt` - Corporate Law and Governance
6. `consumer_protection.txt` - Consumer Protection
7. `digital_rights.txt` - Digital Rights and Cyber Law

#### Medicine Domain (6 documents)
1. `cardiology.txt` - Cardiology and Heart Disease
2. `neurology.txt` - Neurology and Brain Health
3. `pharmacology.txt` - Pharmacology and Drug Development
4. `diabetes.txt` - Diabetes and Metabolic Disorders
5. `mental_health.txt` - Mental Health and Psychiatry
6. `preventive_medicine.txt` - Preventive Medicine and Public Health

**Metadata**: See `metadata.json` for detailed information about each document (word count, key terms, summaries).

---

## Generating Documents

### Option 1: Use Provided Prompts

All prompts for generating these documents are available in:
**`docs/document_generation_prompts.md`**

This file contains:
- Detailed Hebrew prompts for all 20 documents
- Instructions for manual generation using Claude/GPT
- Automated generation script template
- Quality verification checklist

### Option 2: Automated Generation

```bash
# Run the generation script (if created)
python scripts/generate_hebrew_documents.py
```

### Verification

After generating documents, verify:
```bash
# Count documents
find data/raw/hebrew_documents -name "*.txt" | wc -l
# Should output: 20

# Check encoding (should show UTF-8)
file -I data/raw/hebrew_documents/technology/*.txt

# Word count check (should be 500-700 per file)
wc -w data/raw/hebrew_documents/technology/*.txt
```

---

## Synthetic Data

### Purpose
Cached synthetic data for experiments that use programmatically generated documents (Experiments 1, 2, 4).

### Why Synthetic?
- **Experiments 1, 2, 4**: Test context window mechanics, not domain knowledge
- **Reproducibility**: Seeded random generation ensures identical results
- **Scalability**: Can generate thousands of documents instantly
- **Ground Truth**: We know exactly what facts are embedded where

### Generation
Synthetic documents are generated at runtime by:
```python
from context_windows_lab.data_generation.document_generator import DocumentGenerator

gen = DocumentGenerator(seed=42)
docs = gen.generate_documents(
    num_docs=20,
    words_per_doc=200,
    fact="The secret code is BLUE_7293.",
    fact_position="middle"
)
```

See `src/context_windows_lab/data_generation/document_generator.py` for details.

---

## Loading Data in Experiments

### Experiment 3: Load Hebrew Documents

```python
from pathlib import Path

def load_hebrew_documents():
    """Load all Hebrew documents from data/raw/hebrew_documents/"""
    docs_path = Path("data/raw/hebrew_documents")
    documents = []

    for domain_dir in ["technology", "law", "medicine"]:
        domain_path = docs_path / domain_dir
        for txt_file in domain_path.glob("*.txt"):
            content = txt_file.read_text(encoding="utf-8")
            documents.append({
                "domain": domain_dir,
                "filename": txt_file.name,
                "content": content,
                "word_count": len(content.split())
            })

    return documents
```

### Experiments 1, 2, 4: Generate Synthetic

```python
from context_windows_lab.data_generation.document_generator import DocumentGenerator

gen = DocumentGenerator(seed=42)
docs = gen.generate_documents(num_docs=5, words_per_doc=200, ...)
```

---

## Data Quality Standards

### Hebrew Documents
- **Encoding**: UTF-8 (critical for Hebrew text)
- **Language**: Natural Hebrew (not machine translation)
- **Length**: 500-700 words
- **Content**: Informative, well-structured, domain-appropriate
- **Terminology**: Accurate technical/legal/medical terms

### Synthetic Documents
- **Reproducibility**: Seeded generation
- **Fact Embedding**: Clear, verifiable facts
- **Length**: Configurable (typically 200 words)
- **Structure**: Multiple paragraphs with varied templates

---

## Metadata Format

`metadata.json` structure:
```json
{
  "collection_name": "Hebrew Documents for Context Windows Lab",
  "language": "hebrew",
  "total_documents": 20,
  "encoding": "UTF-8",
  "documents": [
    {
      "id": "tech_001",
      "filename": "ai_machine_learning.txt",
      "domain": "technology",
      "topic": "Artificial Intelligence and Machine Learning",
      "topic_hebrew": "בינה מלאכותית ולמידת מכונה",
      "word_count": 650,
      "key_terms": ["בינה מלאכותית", "למידת מכונה", "אלגוריתמים"],
      "summary": "Overview of AI/ML concepts and applications"
    }
  ]
}
```

---

## Data Versioning

- **Git Tracking**: All documents committed to repository
- **Encoding**: UTF-8 (specified in `.gitattributes` if needed)
- **Immutability**: Once generated and tested, avoid modifications
- **Versioning**: Use git tags or branches for major data updates

---

## Benefits of This Organization

1. **Transparency**: All data visible and inspectable
2. **Reproducibility**: Clear generation process documented
3. **Version Control**: All changes tracked in git
4. **Separation**: Raw vs synthetic data clearly separated
5. **Scalability**: Easy to add new documents or domains
6. **Testing**: Can manually verify RAG retrieval quality

---

## Common Issues & Solutions

### Issue: Hebrew Text Not Displaying Correctly
**Solution**: Ensure file encoding is UTF-8
```bash
# Convert if needed
iconv -f ISO-8859-8 -t UTF-8 input.txt > output.txt
```

### Issue: Word Count Incorrect
**Solution**: Hebrew word boundaries differ from English
```python
# Use proper tokenization
import re
words = len(re.findall(r'\S+', hebrew_text))
```

### Issue: Missing Documents
**Solution**: Check directory structure and file permissions
```bash
ls -la data/raw/hebrew_documents/{technology,law,medicine}/
```

---

## Future Enhancements

- [ ] Add English translations for comparison
- [ ] Include real-world documents from open sources
- [ ] Add more domains (science, history, economics)
- [ ] Create multilingual corpus (Arabic, Russian)
- [ ] Add document difficulty ratings
- [ ] Include question-answer pairs for evaluation

---

## References

- **Assignment PDF**: `context-windows-lab.pdf`
- **Generation Prompts**: `docs/document_generation_prompts.md`
- **Data Flow Explanation**: `docs/data_flow_explanation.md`
- **Project Documentation**: `README.md` (root directory)

---

**Last Updated**: 2025-12-10
**Maintained By**: Context Windows Lab Team
**Contact**: See project README for support
