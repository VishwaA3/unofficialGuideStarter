# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

This system makes student-generated knowledge about surviving freshman year at NJIT searchable and answerable. It covers practical topics like registration, parking, food, disability accommodations, orientation, and whether NJIT is worth the cost. This is the kind of advice upperclassmen share informally but new students struggle to find it all in one place. Official NJIT resources rarely capture this raw perspective of navigating the first week feels of being a freshman, leaving incoming students to rely on Reddit threads and word-of-mouth to get useful answers.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1  | r/NJTech | Reddit thread | https://www.reddit.com/r/NJTech/comments/cq8oi8/my_guide_to_computer_science_at_njit/ |
| 2  | r/NJTech | Reddit thread | https://www.reddit.com/r/NJTech/comments/4wx1xv/some_tips_to_all_incoming_freshmen_more_commuter/ |
| 3  | r/NJTech | Reddit thread | https://www.reddit.com/r/NJTech/comments/1t7be07/faq_for_incoming_freshmen/ |
| 4  | r/NJTech | Reddit thread | https://www.reddit.com/r/NJTech/comments/1jc2ayt/is_njit_worth_20k_a_year_in_debt_in_your_opinion/ |
| 5  | r/NJTech | Reddit thread | https://www.reddit.com/r/NJTech/comments/1q3u5gm/how_supportive_is_njit_for_disability_students/ |
| 6  | r/NJTech | Reddit thread | https://www.reddit.com/r/NJTech/comments/1n03vat/what_are_some_costefficient_or_free_ways_i_can/ |
| 7  | r/NJTech | Reddit thread | https://www.reddit.com/r/NJTech/comments/bwv0tk/solid_food_around_njit/ |
| 8  | r/NJTech | Reddit thread | https://www.reddit.com/r/NJTech/comments/3el6hm/new_to_njit_got_questions_ask_them_here/ |
| 9  | r/NJTech | Reddit thread | https://www.reddit.com/r/NJTech/comments/1lbme48/for_upcoming_first_years/ |
| 10 | r/NJTech | Reddit thread | https://www.reddit.com/r/NJTech/comments/1mu07w0/nso_20_why_is_it_almost_a_full_day/ |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 500 characters

**Overlap:** 100 characters

**Why these choices fit your documents:** My documents are a mix of short student tips, Q&A threads, and longer structured guides from r/NJTech. A 500-character chunk is large enough to capture a complete thought or piece of advice without merging unrelated topics together. Chunks smaller than this risk cutting advice mid-sentence, making them useless on their own. A 100-character overlap ensures that advice split across a chunk boundary is still retrievable — if a key tip starts at the end of one chunk, the next chunk will also contain its beginning. Before chunking, documents were manually cleaned to remove Reddit UI elements such as upvote/downvote counts, usernames, award icons, and promoted content. Each chunk is stored with its source filename as metadata for attribution.

**Final chunk count:** 82 chunks across 10 source documents

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2 via sentence-transformers

**Production tradeoff reflection:**
For this project, all-MiniLM-L6-v2 via sentence-transformers is a great fit, considering how it is fast, free, and runs locally with no rate limits. It handles short and conversationally-styled text properly, which is ideal considering the Reddit-styled content in my documents. 
If I was deploying this project for real users and cost wasn't a constraint, the following are tradeoffs I'd weigh in when it comes to choosing a different embedding model. 

- **Context Length:** When it comes to context length, all-MiniLM-L6-v2 has a 256-token limit per chunk. This means that longer documents, such as advice guides that can span till multiple paragraphs, would cut off useful content. A model with a greater token limit would allow greater chunk sizes, preventing them from getting cut off when the token limit is reached. 
- **Multilingual Support:**  For multilingual support, I'd use a multilingual model considering the fact that NJIT has a large international student population. A multilingual model would allow non-English speakers to query in their native languages as well. 
- **Accuracy on Domain-Specific Text:** A model that is trained on student or forum-styled text, for example: Reddit data, would retrieve more relevant chunks of data for more casual and quick-questions styled queries. 
- **Latency:** For a personal project like this one, the smaller/local model is efficient, providing quicker responses with no cost. However, a larger model that is trained on way more data and contains a lot more layers holds a better ability to understand specific and complex queries. However, with a greater model comes latency. When it comes to a real app with real users, I'd need to carefully compare and analyze whether the accuracy that comes with a larger model is worth it for the latency and cost.  

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
You are a helpful assistant for incoming NJIT freshmen.
Answer questions using ONLY the information provided in the context below.
If the context does not contain enough information to answer the question, say "I don't have enough information on that in my documents."
Always end your response with a "Sources:" section listing the document names you used.
Do not make up information or use outside knowledge.

**How source attribution is surfaced in the response:**
Source attribution is handled in two ways. 
First, the system prompt instructs the LLM to include a "Sources:" section in every response naming the documents it drew from.
Second, the Gradio interface displays a separate "Retrieved from" field that programmatically lists the source filenames of every chunk passed to the LLM as context. This ensures attribution is guaranteed even if the LLM omits it in its response.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What are some free or cheap parking options near NJIT for commuters? | Lock St, Boyden St, Central Ave, $325 pass, NJ Transit student pass | Listed all free streets correctly, mentioned day pass option | Relevant | Accurate |
| 2 | What GPA do you need to stay in good academic standing at NJIT? | 2.0+ Overall and Term GPA, Dean's List 3.0+, Greek Life 2.6+ | Correctly stated 2.0+ in both Overall and Term GPA but did not mention Dean's List or Greek Life GPA requirements | Relevant | Partially accurate |
| 3 | How do disability accommodations work at NJIT through OARS? | Submit to OARS 3-4 days before exams, not professors; get docs in early | Correctly explained full OARS process including 3-4 day form requirement and ADA protections | Relevant | Accurate |
| 4 | What do students say about whether NJIT is worth the cost? | CC first, dorms $5000+, University Centre $800/month, strong salaries | Covered CC advice and debt info correctly but missed University Centre pricing and dorm cost specifics | Partially relevant | Partially accurate |
| 5 | What food spots near NJIT have student discounts? | Burger Walla, Meatball Obsession, Masala Cafe, Fresh Coast, Turkish Pita, Halal Guys | Returned 4 of 6 correctly — missed Masala Cafe and Turkish Pita Place | Partially relevant | Partially accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** "What food spots near NJIT have student discounts?"

**What the system returned:** The system returned 4 out of 6 expected restaurants: Burger Walla, Meatball Obsession, Fresh Coast, and Halal Guys. However, it missed Masala Cafe and Turkish Pita Place.

**Root cause (tied to a specific pipeline stage):** The failure occurred at the retrieval stage. With top-k set to 4, only 4 chunks were passed to the LLM as context. The food guide document (doc7.txt) contains many restaurants spread across multiple chunks. Masala Cafe and Turkish Pita Place happened to fall in chunks that were not ranked in the top 4 by the embedding model because their distance scores were high and caused them to get pushed out of the retrieved set. This is a consequence of the top-k limit combined with relevant information being spread across multiple chunks in the same document.

**What you would change to fix it:** Increasing top-k from 4 to 6/7 for food-related queries would likely surface the missing chunks. Or, another option could be to use a smaller chunk for the food guide document specifically would give each restaurant entry into its own chunk, making individual entries easier to retrieve precisely.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** Writing the chunking strategy in planning.md before touching any code forced me to think about what chunk size actually fit my documents. Because I had already decided on 500 characters and 100-character overlap with reasoning written out, I could give Claude a specific, concrete spec to implement rather than asking it to make those decisions for me. This made the generated ingest.py match my system exactly on the first try rather than requiring significant revision.

**One way your implementation diverged from the spec, and why:** In the spec, I anticipated that residual noise in Reddit threads would be a significant challenge for retrieval. In practice, manually cleaning all 10 documents before ingestion removed most of the noise, so this risk was largely mitigated before the pipeline was even built. The actual failure that emerged was different from what I anticipated — it was a top-k coverage problem rather than a noise problem, where relevant chunks existed in the vector store but were not ranked highly enough to be retrieved. 

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* My Chunking Strategy section from planning.md (500 characters, 100 overlap, .txt files in /sources folder) and my pipeline diagram showing the five stages of the system.
- *What it produced:* A complete ingest.py script with load_documents(), chunk_text(), and build_chunks() functions that matched my specified chunk size and overlap and attached source filenames as metadata to each chunk.
- *What I changed or overrode:* The generated code was correct and matched the spec. I verified it by printing 5 sample chunks and confirming they were under 500 characters, readable, and had source metadata attached. No changes were needed.

**Instance 2**

- *What I gave the AI:* My Retrieval Approach section from planning.md (all-MiniLM-L6-v2, ChromaDB, top-k=4) and my grounding requirement (answers from retrieved context only, with source attribution).
- *What it produced:* embed.py with embedding and ChromaDB storage, query.py with a grounded system prompt and Groq integration, and app.py with a Gradio interface containing a question input, answer output, and sources output.
- *What I changed or overrode:* The system prompt in the generated query.py used vague grounding language. I directed the AI to strengthen it by explicitly instructing the model to say "I don't have enough information on that in my documents" for out-of-scope questions rather than causing hallucinations.