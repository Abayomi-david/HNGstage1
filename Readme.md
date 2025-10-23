#  String Analyzer Service — Backend Wizards (Stage 1)

A **RESTful API** built with **Python FastAPI** that analyzes strings and stores their computed properties.

---

##  Features

For each analyzed string, the API computes and stores:

- **length** → number of characters  
- **is_palindrome** → case-insensitive check  
- **unique_characters** → count of distinct characters  
- **word_count** → number of words separated by whitespace  
- **sha256_hash** → SHA-256 hash (unique identifier)  
- **character_frequency_map** → dictionary mapping characters → count  

### Endpoints
- `POST /strings` — Create & analyze string  
- `GET /strings/{string_value}` — Get details of a specific string  
- `GET /strings` — List all strings with filtering  
- `GET /strings/filter-by-natural-language` — Filter via natural language queries  
- `DELETE /strings/{string_value}` — Delete a specific string  
- `GET /health` — Check server health  

---

##  Example Computation

Analyzing `"racecar"` returns:
```json
{
  "id": "3a0a94fdbb...",
  "value": "racecar",
  "properties": {
    "length": 7,
    "is_palindrome": true,
    "unique_characters": 4,
    "word_count": 1,
    "sha256_hash": "3a0a94fdbb...",
    "character_frequency_map": {
      "r": 2,
      "a": 2,
      "c": 2,
      "e": 1
    }
  },
  "created_at": "2025-08-27T10:00:00Z"
}


Assumptions

is_palindrome is case-insensitive, ignores leading/trailing spaces, but does not remove punctuation.

unique_characters is case-sensitive.

word_count uses standard whitespace splitting.

sha256_hash uniquely identifies each string.

character_frequency_map preserves actual characters.