export type PageResponse<T> = {
  "page_number": number
  "page_size": number,
  "total_pages": number,
  "total_records": number,
  "content": T[],
  "content_meta": {
    "investor_name": string,
    "total_commitment": number,
    "total_commitments": Record<string, number>,
    "total_commitments_per_asset_class": Record<string, number>,
  }
}

export type Commitment = {
  "commitment_id": string
  "commitment_asset_class": string
  "commitment_currency": string
  "commitment_amount": number
}

export type Investor = {
  "investor_id": string
  "investor_name": string
  "investory_type": string
  "investor_date_added": string
  "investor_country": string
}