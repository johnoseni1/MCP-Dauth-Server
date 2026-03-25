

API_KEY="dsk-test-28fa7d847893-7a35d8505301d54e919df7a257b55c32"


MCP_SERVER="littlbird/MCP-Dauth-Server"

echo "======================================================="
echo "  DAuth MCP Server — Direct REST API Test (cURL)"
echo "  Server : $MCP_SERVER"
echo "======================================================="
echo ""
echo "Sending request to Dedalus Inference Gateway..."

curl -s -X POST https://api.dedaluslabs.ai/v1/chat/completions \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-4.1",
    "messages": [
      {
        "role": "user",
        "content": "Calculate the final price for an item that costs $100 with a 20% discount and 7.5% tax. Use the calculate_discount tool."
      }
    ],
    "mcp_servers": ["'$MCP_SERVER'"]
  }' | jq '.'
