from __future__ import annotations
from typing import Dict, List, Any
import pandas as pd
from io import StringIO

def analyze_csv_data(csv_string: str) -> Dict:
    """Analyze CSV string data (Calculate mean, sum, max)"""
    try:
        df = pd.read_csv(StringIO(csv_string))
        
        # Numeric/String separation is good practice
        numeric_df = df.select_dtypes(include=['number'])
        
        stats = {
            "rows": len(df),
            "columns": list(df.columns),
            "numeric_summary": numeric_df.describe().to_dict()
        }
        return {"success": True, "stats": stats}
    except Exception as e:
        return {"success": False, "error": str(e)}


def transform_json_data(data: List[Dict], operations: List[Dict]) -> List[Dict]:
    """Transform a list of dictionaries. Operations: uppercase, scale"""
    result = [d.copy() for d in data]
    
    for op in operations:
        op_type = op.get('type')
        field = op.get('field')
        
        if op_type == 'uppercase':
            for d in result:
                if field in d and isinstance(d[field], str):
                    d[field] = d[field].upper()
                    
        elif op_type == 'scale':
            factor = op.get('factor', 1)
            for d in result:
                if field in d and isinstance(d[field], (int, float)):
                    d[field] = d[field] * factor
                    
    return result


def filter_data(data: List[Dict], conditions: Dict) -> List[Dict]:
    """Filter list of dicts based on exact match conditions"""
    filtered = []
    for item in data:
        match = True
        for k, v in conditions.items():
            if item.get(k) != v:
                match = False
                break
        if match:
            filtered.append(item)
    return filtered


def aggregate_data(data: List[Dict], group_by: str, metric_field: str, metric: str = 'sum') -> Dict:
    """Group by a field and calculate a metric (sum, avg, count)"""
    try:
        df = pd.DataFrame(data)
        if group_by not in df.columns or metric_field not in df.columns:
            return {"error": "Invalid columns"}
            
        grouped = df.groupby(group_by)[metric_field]
        
        if metric == 'sum':
            res = grouped.sum()
        elif metric == 'avg':
            res = grouped.mean()
        elif metric == 'count':
            res = grouped.count()
        else:
            return {"error": "Unsupported metric"}
            
        return res.to_dict()
    except Exception as e:
        return {"error": str(e)}


def merge_datasets(data1: List[Dict], data2: List[Dict], key: str) -> List[Dict]:
    """Merge two datasets on a common key (Inner Join)"""
    try:
        df1 = pd.DataFrame(data1)
        df2 = pd.DataFrame(data2)
        merged = pd.merge(df1, df2, on=key, how='inner')
        return merged.to_dict(orient='records')
    except Exception as e:
        return {"error": str(e)}
