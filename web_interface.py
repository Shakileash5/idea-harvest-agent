#!/usr/bin/env python3
"""
Web interface for Idea Harvest Agent
Simple Flask app to interact with the harvesting system
"""

from flask import Flask, render_template, jsonify, request, send_file
import json
import os
from datetime import datetime
from main import IdeaHarvestAgent

app = Flask(__name__)
agent = IdeaHarvestAgent()

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')

@app.route('/api/harvest', methods=['POST'])
def start_harvest():
    """Start the harvesting process"""
    try:
        # Run harvest in background (in production, use Celery or similar)
        results = agent.harvest_all_sources()
        return jsonify({
            'success': True,
            'message': 'Harvest completed',
            'data': results
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/process', methods=['POST'])
def process_problems():
    """Process and cluster problems"""
    try:
        clusters = agent.process_problems()
        return jsonify({
            'success': True,
            'message': 'Processing completed',
            'clusters': len(clusters)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/ideas', methods=['POST'])
def generate_ideas():
    """Generate product ideas"""
    try:
        ideas = agent.generate_ideas()
        return jsonify({
            'success': True,
            'message': 'Ideas generated',
            'ideas': len(ideas)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/playbooks', methods=['POST'])
def create_playbooks():
    """Create validation playbooks"""
    try:
        playbooks = agent.create_validation_playbooks()
        return jsonify({
            'success': True,
            'message': 'Playbooks created',
            'playbooks': len(playbooks)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/results')
def get_results():
    """Get current results"""
    return jsonify(agent.results)

@app.route('/api/export/json')
def export_json():
    """Export results as JSON"""
    filename = agent.save_results()
    return send_file(filename, as_attachment=True)

@app.route('/api/export/markdown')
def export_markdown():
    """Export results as Markdown"""
    filename = agent.generate_markdown_report()
    return send_file(filename, as_attachment=True)

@app.route('/api/run-full', methods=['POST'])
def run_full_pipeline():
    """Run the complete pipeline"""
    try:
        results = agent.run_full_pipeline()
        return jsonify({
            'success': True,
            'message': 'Full pipeline completed',
            'results': results
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

if __name__ == '__main__':
    import sys
    import socket
    
    def find_free_port():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            return s.getsockname()[1]
    
    if '--port' in sys.argv:
        port = int(sys.argv[sys.argv.index('--port') + 1])
    else:
        port = find_free_port()
    
    print(f"🚀 Starting web interface on http://localhost:{port}")
    app.run(debug=True, host='0.0.0.0', port=port)
