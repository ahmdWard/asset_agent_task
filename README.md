
##  Features

### Backend API
-  Full CRUD operations (Create, Read, Update, Delete)
-  Advanced filtering (category, status, value range, date range, search)
-  Sorting and pagination
-  Soft delete support
-  Input validation with Pydantic
-  Auto-generated API documentation

### AI Agent
-  Natural language query processing
-  Multi-tool architecture (search assets, get by ID)
-  Automatic asset ID tracking in responses
-  Smart filtering and calculations
-  Error handling and fallbacks

### Bonus Features Implemented Done 
-  Advanced asset search/filtering on the API
### NOT yet
-   memory 
-  Token monitoring 

##  Tech Stack

- **Backend Framework:** FastAPI 
- **Database:** SQLite
- **AI Agent:** LangChain + OpenAI GPT-4o-mini


### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/ahmdWard/asset_agent_task.git
cd asset_agent_task
```

2. **Create virtual environment**
```bash
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
# Create .env file
# OPEN_API_KEY=your-openai-api-key-here
# DATABASE_URL=sqlite:///./assets.db
```

5. **Run the application**
```bash
uvicorn app.main:app --reload
```

The API will be available at: **http://127.0.0.1:8000**

## API Documentation

Once the server is running, access the interactive documentation:

- **Swagger UI:** http://127.0.0.1:8000/docs

##  API Endpoints

### Assets (CRUD Operations)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/assets` | Create a new asset |
| GET | `/api/v1/assets` | List all assets (with filtering) |
| GET | `/api/v1/assets/{id}` | Get asset by ID |
| PUT | `/api/v1/assets/{id}` | Update an asset |
| DELETE | `/api/v1/assets/{id}` | Delete asset (soft delete by default) |

### AI Agent

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/agent/query` | Ask natural language questions about assets |

##  Usage Examples

### Creating an Asset

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/assets" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MacBook Pro 16-inch",
    "category": "electronics",
    "value": 2500,
    "purchase_date": "2024-01-15",
    "status": "active",
    "description": "M3 Pro chip, 32GB RAM"
  }'
```

### Listing Assets with Filters

```bash
# Get all electronics under $1000
curl "http://127.0.0.1:8000/api/v1/assets?category=electronics&max_value=1000"

# Get assets purchased in 2024, sorted by value
curl "http://127.0.0.1:8000/api/v1/assets?purchase_date_from=2024-01-01&sort_by=value&order=desc"

# Search for "laptop" in names/descriptions
curl "http://127.0.0.1:8000/api/v1/assets?search=laptop"
```

### Updating an Asset

```bash
curl -X PUT "http://127.0.0.1:8000/api/v1/assets/{asset_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "value": 2200,
    "status": "sold"
  }'
```

### Deleting an Asset

```bash
# Soft delete (default  keeps in database, marks as deleted)
curl -X DELETE "http://127.0.0.1:8000/api/v1/assets/{asset_id}"

# Hard delete (permanently removes from database)
curl -X DELETE "http://127.0.0.1:8000/api/v1/assets/{asset_id}?hard=true"
```

##  AI Agent

### Querying with Natural Language

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/agent/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is my most valuable asset?"
  }'
```

**Response:**
```json
{
  "answer": "Your most valuable asset is the MacBook Pro valued at $2,500",
  "sources": ["asset-uuid-123"],
  "query_type": "success",
  "assets_found": 1
}
```

### Example Questions for the AI Agent

**Asset Discovery:**
- "What assets do I have?"
- "Show me all my electronics"
- "Do I have any furniture?"
- "List assets worth more than $1000"

**Value Queries:**
- "What is my most valuable asset?"
- "What's my cheapest item?"
- "What's my total portfolio value?"
- "How much did I spend on electronics?"

**Category & Status:**
- "Show me active assets"
- "What electronics do I own?"
- "List all sold items"

**Specific Items:**
- "Tell me about my MacBook"
- "Show details of my office chair"

### Agent Response Format

```json
{
  "answer": "Natural language response to your question",
  "sources": ["asset-uuid-1", "asset-uuid-2"],
  "query_type": "success|error",
  "assets_found": 2
}
```

| Field | Description |
|-------|-------------|
| `answer` | The AI's natural language response |
| `sources` | Array of asset UUIDs referenced in the answer |
| `query_type` | Status of the query (success/error) |
| `assets_found` | Number of unique assets referenced |

##  Asset Schema

### Asset Model

```json
{
  "id": "uuid-string",
  "name": "MacBook Pro 16-inch",
  "category": "electronics",
  "value": 2500.00,
  "purchase_date": "2024-01-15",
  "status": "active",
  "description": "M3 Pro chip, 32GB RAM",
  "is_deleted": false,
  "deleted_at": null,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

### Valid Categories
- `electronics`
- `furniture`
- `vehicle`
- `appliance`
- `jewelry`
- `other`

### Valid Statuses
- `active`
- `sold`
- `damaged`
- `lost`
- `donated`
- `inactive`

##  Advanced Filtering

The GET `/api/v1/assets` endpoint supports comprehensive filtering:

### Query Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `category` | string | Filter by category | `electronics` |
| `status` | string | Filter by status | `active` |
| `min_value` | float | Minimum asset value | `500` |
| `max_value` | float | Maximum asset value | `5000` |
| `purchase_date_from` | date | Start date (YYYY-MM-DD) | `2024-01-01` |
| `purchase_date_to` | date | End date (YYYY-MM-DD) | `2024-12-31` |
| `search` | string | Search in name/description | `laptop` |
| `sort_by` | string | Field to sort by | `value`, `name`, `created_at` |
| `order` | string | Sort order | `asc` or `desc` |
| `skip` | integer | Pagination offset | `0` |
| `limit` | integer | Items per page (max 1000) | `100` |

### Filtering Examples

```bash
# Complex filter: Electronics between $500-$2000, purchased in 2024
curl "http://127.0.0.1:8000/api/v1/assets?category=electronics&min_value=500&max_value=2000&purchase_date_from=2024-01-01&purchase_date_to=2024-12-31&sort_by=value&order=desc"
```

##  Project Structure

```
asset_agent_task/
├── app/
│   ├── __init__.py
│   ├── main.py              
│   ├── agent.py             
│   ├── config.py           
│   ├── database.py          
│   ├── models.py            
│   ├── schemas.py           
│   └── routes/
│       ├── __init__.py
│       └── crud.py          
├── .env                     
├── .env.example             
├── .gitignore              
├── requirements.txt         
└── README.md               
```

### AI Agent
- **Model:** OpenAI GPT-4o-mini 
- **Temperature:** 0 (deterministic responses)
- **Max iterations:** 5 (prevents infinite loops)
- **Tools:** search_assets, get_asset_by_id
- **Verbose mode:** Enabled (see agent thinking in terminal)