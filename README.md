# rate-my-professor-api
API for Rate My Professor (CSULB only)

## Installation

## API documentation

### 1. `/`

- Queries

  1. `?by (required)`: "college"|"subject"|"ge"
  2. `?query (required)`: 
    - When 'by' is either "college" or "subject" => Course code
    - When 'by' is "ge" => GE area code
  3. `?rating`: Less than or equal to 5
