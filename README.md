# UTBK RAG Tutor 🎓

An AI-powered tutoring application that helps students answer UTBK (Ujian Tulis Berbasis Komputer) exam questions and generate new practice questions using Retrieval-Augmented Generation (RAG) technology.

## Features

- **Question Answering**: Get detailed answers to UTBK exam questions with source citations
- **Question Generation**: Automatically generate new multiple-choice questions (MCQ) from reference materials
- **Source Traceability**: All answers cite the specific documents and pages used
- **RAG Technology**: Uses vector search to retrieve relevant context before generating responses
- **Structured Output**: Generated questions follow JSON format with explanations

## Prerequisites

- **Python 3.8+** installed on your system
- **OpenRouter API Key** (for LLM access)
- **OpenAI API Key** (for embeddings - optional, can use local embeddings)
- **Internet connection** (to communicate with APIs)

## Installation

### 1. Clone or Download the Project

```bash
cd your-project-directory
```

### 2. Install Python Dependencies

Install all required packages using pip:

```bash
pip install -r requirements.txt
```

**Required packages:**
- streamlit - Web interface framework
- langchain - LLM orchestration
- langchain-community - LangChain integrations
- chromadb - Vector database
- pypdf - PDF parsing
- openai - OpenAI API client
- python-dotenv - Environment configuration
- tiktoken - Token counting

### 3. Configure Environment Variables

Create a `.env` file in the project root directory with the following variables:

```env
# OpenRouter API Configuration
OPENAI_API_KEY=sk-or-v1-your-openrouter-api-key-here
OPENAI_API_BASE=https://openrouter.ai/api/v1

# Model Configuration
CHAT_MODEL=openai/gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small
```

**How to get API keys:**
1. **OpenRouter API Key**: Visit https://openrouter.ai, sign up, and generate an API key from your dashboard
2. **OpenAI API Key**: Visit https://platform.openai.com, sign up, and create an API key (or use OpenRouter's key for both)

### 4. Prepare Your Data

Place PDF documents in the `data/` folder:

```
project-root/
└── data/
    ├── SAINTEK - MASUKUTBK September 2022.pdf
    ├── Soal_SBMPTN_SAINTEK.pdf
    └── TPS - MASUKUTBK September 2022.pdf
```

## Usage

### Step 1: Build the Vector Database

Before running the application for the first time, you need to ingest your PDF documents and create a searchable vector store:

```bash
python ingest.py
```

**What this does:**
- Reads all PDF files from the `data/` folder
- Splits documents into chunks (1200 characters with 150 character overlap)
- Creates embeddings using the specified embedding model
- Stores indexed data in the `vectorstore/` folder using Chroma

**Output:**
- Creates `vectorstore/` directory with SQLite database files
- This process only needs to run once (or when you add new PDFs)

### Step 2: Run the Application

Start the Streamlit web interface:

```bash
streamlit run app.py
```

**Expected output:**
```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Open your browser and navigate to `http://localhost:8501`

### Step 3: Use the Application

The web interface has two main features:

#### Feature 1: "Jawab Soal" (Answer Questions)

1. Go to the **"Jawab Soal"** tab
2. Paste or type an exam question in the text area
3. Click **"Generate Jawaban"** button
4. The system will:
   - Search for relevant content in your PDF documents
   - Generate a detailed answer using AI
   - Display the answer with source citations (document name and page number)

**Example input:**
```
Apa yang dimaksud dengan fotosintesis?
```

**Example output:**
```
Jawaban:
[Detailed answer from LLM based on retrieved context]

Sumber:
- Document: SAINTEK - MASUKUTBK September 2022.pdf (Page 5)
- Document: Soal_SBMPTN_SAINTEK.pdf (Page 12)
```

#### Feature 2: "Generate Soal" (Generate Questions)

1. Go to the **"Generate Soal"** tab
2. Enter a topic or keyword (e.g., "fotosintesis", "gravitasi")
3. Click **"Generate"** button
4. The system will:
   - Find relevant reference material
   - Generate a new multiple-choice question with 4 options
   - Provide the correct answer and explanation

**Example input:**
```
Topik: Struktur Atom
```

**Example output:**
```json
{
  "soal": "Partikel subatomik dengan muatan negatif adalah...",
  "opsi_a": "Proton",
  "opsi_b": "Neutron",
  "opsi_c": "Elektron",
  "opsi_d": "Positron",
  "jawaban_benar": "C",
  "penjelasan": "Elektron adalah partikel subatomik dengan muatan negatif..."
}
```

## Project Structure

```
aittutordts/
├── app.py                      # Main Streamlit application
├── rag.py                      # RAG engine (retrieval & LLM logic)
├── ingest.py                   # PDF ingestion pipeline
├── prompts.py                  # LLM system prompts
├── utils.py                    # Utility functions
├── requirements.txt            # Python dependencies
├── .env                        # Configuration (API keys, model names)
├── README.md                   # This file
├── data/                       # Input PDF documents
│   ├── SAINTEK - MASUKUTBK September 2022.pdf
│   ├── Soal_SBMPTN_SAINTEK.pdf
│   └── TPS - MASUKUTBK September 2022.pdf
├── vectorstore/                # Chroma vector database (created by ingest.py)
│   ├── chroma.sqlite3
│   └── [vector embeddings]
└── tests/                      # Test directory (for future tests)
```

## File Descriptions

### `app.py`
Main Streamlit application with two tabs:
- **Jawab Soal**: Answer exam questions with source citations
- **Generate Soal**: Generate new multiple-choice questions

### `rag.py`
Core RAG (Retrieval-Augmented Generation) engine:
- `get_retriever()` - Creates vector store retriever
- `get_llm()` - Initializes LLM connection
- `format_context()` - Formats retrieved documents
- `solve_question()` - Answers a question using RAG
- `generate_item()` - Generates a new MCQ

### `ingest.py`
Data ingestion pipeline:
- `build_store()` - Main function that processes PDFs and creates vector database

### `prompts.py`
LLM system prompts:
- `SOLVE_SYS` - Instructions for answering questions
- `GEN_SYS` - Instructions for generating questions

## Configuration

### Model Selection

You can change the LLM model in `.env`:

```env
# Available models on OpenRouter:
CHAT_MODEL=openai/gpt-4o-mini      # Fast and accurate (recommended)
CHAT_MODEL=openai/gpt-4            # More powerful, slower
CHAT_MODEL=meta-llama/llama-2-70b  # Open source option
```

### Temperature Settings

In `rag.py`, you can adjust temperature for different behaviors:

```python
temperature=0.2   # More deterministic, better for answers
temperature=0.4   # Balanced, good for question generation
temperature=0.7   # More creative, varied responses
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'streamlit'"

**Solution:** Reinstall dependencies
```bash
pip install -r requirements.txt
```

### Issue: "Error: OPENAI_API_KEY not found in environment"

**Solution:** Check your `.env` file:
1. Ensure `.env` exists in the project root directory
2. Ensure `OPENAI_API_KEY` is set correctly
3. Save the file and restart the application

### Issue: "No documents found in vectorstore"

**Solution:** Run the ingestion script first
```bash
python ingest.py
```

### Issue: "Cannot find PDF files in data/ folder"

**Solution:**
1. Create a `data/` folder in the project root if it doesn't exist
2. Add your PDF files to this folder
3. Run `python ingest.py` again

### Issue: "Rate limit exceeded" or "API quota exceeded"

**Solution:**
- Check your OpenRouter API quota at https://openrouter.ai
- Wait for the quota to reset
- Or add more credits to your OpenRouter account

### Issue: API Connection Errors

**Solution:**
1. Check your internet connection
2. Verify API keys are correct
3. Ensure OpenRouter is accessible: `curl https://openrouter.ai/api/v1/models`

## Adding New Documents

To add new PDF documents to the system:

1. Place your PDF files in the `data/` folder
2. Run the ingestion script again:
   ```bash
   python ingest.py
   ```
3. Restart the Streamlit application

The system will automatically process new PDFs and update the vector database.

## Technology Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit |
| **LLM Provider** | OpenRouter (OpenAI-compatible API) |
| **Vector Database** | Chroma |
| **LLM Embeddings** | text-embedding-3-small |
| **LLM Framework** | LangChain |
| **Document Processing** | PyPDF |
| **Language** | Python 3 |

## Architecture

```
User Input (Question/Topic)
    ↓
Query Vector Store → Retrieve Top 5 Documents
    ↓
Format Retrieved Context
    ↓
Prompt LLM with System Instructions
    ↓
Generate Response
    ↓
Display Result + Source Citations
```

## Performance Tips

1. **Optimize chunk size**: In `ingest.py`, adjust `chunk_size` and `chunk_overlap` for better results
   ```python
   chunk_size=1200        # Increase for more context
   chunk_overlap=150      # Overlap helps maintain context between chunks
   ```

2. **Adjust retrieval count**: In `rag.py`, modify the number of retrieved documents
   ```python
   retriever = vectorstore.as_retriever(search_kwargs={"k": 5})  # Change 5 to 3-10
   ```

3. **Temperature tuning**: Lower temperature (0.2) for consistent answers, higher (0.7) for variety

## Limitations & Notes

- The system is restricted to answer only from provided PDFs (by design)
- Answers quality depends on the quality and relevance of source documents
- Generated questions may sometimes need manual review
- Internet connection required for API calls
- All API calls incur costs based on OpenRouter pricing

## Support & Feedback

For issues or feature requests, please check:
- Your `.env` configuration
- API key validity and remaining quota
- PDF file format (must be standard PDFs)
- Internet connection stability

## License

[Add your license information here]

## Author

[Add your name/organization here]

---

**Last Updated:** November 2025
**Python Version:** 3.8+
**Status:** Active Development
