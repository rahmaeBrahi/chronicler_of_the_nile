from flask import Blueprint, jsonify
import json
import os

knowledge_bp = Blueprint('knowledge', __name__)

def load_knowledge_base():
    """Load historical knowledge from JSON files"""
    knowledge_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'knowledge_base')
    knowledge = {}
    
    knowledge_files = [
        'ancient_egypt.json',
        'graeco_roman.json', 
        'islamic_ottoman.json',
        'modern_egypt.json'
    ]
    
    for filename in knowledge_files:
        filepath = os.path.join(knowledge_dir, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    period_name = filename.replace('.json', '')
                    knowledge[period_name] = json.load(f)
            except Exception as e:
                print(f"Error loading {filename}: {e}")
                knowledge[period_name] = {}
        else:
            period_name = filename.replace('.json', '')
            knowledge[period_name] = {}
    
    return knowledge

@knowledge_bp.route('/knowledge', methods=['GET'])
def get_all_knowledge():
    """Get all historical knowledge"""
    try:
        knowledge = load_knowledge_base()
        return jsonify(knowledge)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@knowledge_bp.route('/knowledge/<period>', methods=['GET'])
def get_period_knowledge(period):
    """Get knowledge for a specific historical period"""
    try:
        knowledge = load_knowledge_base()
        
        if period in knowledge:
            return jsonify({
                'period': period,
                'data': knowledge[period]
            })
        else:
            return jsonify({'error': f'Period {period} not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@knowledge_bp.route('/knowledge/periods', methods=['GET'])
def get_periods():
    """Get list of available historical periods"""
    try:
        knowledge = load_knowledge_base()
        periods = list(knowledge.keys())
        
        return jsonify({
            'periods': periods,
            'count': len(periods)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

