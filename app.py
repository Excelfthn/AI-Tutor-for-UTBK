import os
import json
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from rag import get_retriever, get_llm, solve_question, generate_item

st.set_page_config(page_title="UTBK RAG Tutor", layout="wide")
st.title("UTBK RAG Tutor")

# Cek API key
if not os.getenv("OPENAI_API_KEY"):
    st.error("OPENAI_API_KEY belum di-set (pakai key OpenRouter). Cek file .env")
if not os.getenv("OPENAI_API_BASE"):
    st.warning("OPENAI_API_BASE belum di-set. Default OpenRouter: https://openrouter.ai/api/v1")

retriever = get_retriever()
llm_solve = get_llm(temperature=0.2)
llm_gen   = get_llm(temperature=0.4)

tab1, tab2 = st.tabs(["Jawab Soal", "Generate Soal"])

with tab1:
    st.subheader("Jawab Soal UTBK (berbasis referensi)")
    q = st.text_area("Tempel soal di sini:", height=160, placeholder="Contoh: Diketahui fungsi f(x)= ...")
    if st.button("Jawab"):
        if not q.strip():
            st.warning("Isi dulu soalnya.")
        else:
            with st.spinner("Mengambil konteks & menyusun jawaban..."):
                ans, used_docs = solve_question(q, retriever, llm_solve)
            st.markdown("### Jawaban")
            st.write(ans)
            with st.expander("Sumber yang dipakai"):
                for d in used_docs:
                    st.write(f"- {d.metadata.get('source')} (hal. {d.metadata.get('page')})")

with tab2:
    st.subheader("Generate 1 Soal dari Referensi (MCQ)")
    t = st.text_input("Topik / Kata kunci (mis. Trigonometri, Stoikiometri, Laju Reaksi, dll)")
    if st.button("Generate Soal"):
        if not t.strip():
            st.warning("Isi dulu topik/kata kunci.")
        else:
            with st.spinner("Mengambil konteks & membuat soal..."):
                item_json, used_docs = generate_item(t, retriever, llm_gen)

            st.markdown("### Hasil (JSON)")
            st.code(item_json, language="json")

            # Validasi sederhana
            try:
                obj = json.loads(item_json)
                ok = isinstance(obj.get("options"), list) and obj.get("answer_key") in "".join(obj.get("options", []))
                st.success("JSON valid." if ok else "JSON terbuat tetapi perlu cek konsistensi kunci/options.")
            except Exception as e:
                st.error(f"JSON tidak valid: {e}")

            with st.expander("Sumber yang dipakai"):
                for d in used_docs:
                    st.write(f"- {d.metadata.get('source')} (hal. {d.metadata.get('page')})")
