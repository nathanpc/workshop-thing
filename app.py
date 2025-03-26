#!/usr/bin/env python

import yaml
import os.path
from flask import Flask, abort, request, render_template, make_response

from quickpoll import Poll

# Define the global flask application object.
app = Flask(__name__, static_url_path='')
poll_cache = None


def load_polls():
    """Loads up the polls from the configuration file."""
    global poll_cache
    polls = []
    polls_fpath = Poll.config_file()

    # Check if the polls file actually exists.
    if not os.path.exists(polls_fpath):
        print(f'Polls configuration file ({polls_fpath}) doesn''t exist.')
        exit(1)

    with open(polls_fpath, 'r') as stream:
        # Load the configuration from our YAML file.
        config = yaml.safe_load(stream)

        # Populate the polls.
        for p in config['polls']:
            polls.append(Poll.from_dict(p))

    poll_cache = polls


def get_poll_from_name(name):
    """Gets a poll from our poll list by its name."""
    global poll_cache

    for poll in poll_cache:
        if poll.name == name:
            return poll

    return None


@app.route('/')
def render_index():
    """Renders the main page template."""
    return render_template('index.html', polls=poll_cache)


@app.route('/poll/<name>')
def render_poll(name):
    """Renders the single poll template."""
    poll = get_poll_from_name(name)
    if poll is not None:
        return render_template('single_poll.html', poll=poll.__dict__)

    # No matching poll was found.
    abort(404)


@app.route('/results')
def render_results():
    """Renders the results page template."""
    return render_template('results.html', polls=poll_cache)


@app.route('/export/csv')
def export_csv():
    """Exports the results as CSV."""
    # Build up the CSV file.
    csv = '"poll_name","poll_title","poll_option_value","poll_option_label","poll_option_votes",\r\n'
    for poll in poll_cache:
        for opt in poll.options:
            csv += f'"{poll.name}","{poll.title}","{opt.value}","{opt.label}","{opt.votes}",\r\n'

    # Build up the response.
    response = make_response(csv)
    response.headers['Content-Type'] = 'text/csv'
    return response

@app.route('/api/polls')
def list_polls():
    """Gets the list of the available polls."""
    global poll_cache
    json = {'polls': []}

    for poll in poll_cache:
        json['polls'].append(poll.__dict__)

    return json


@app.route('/api/poll/<name>')
def get_poll(name):
    """Gets a specific poll by its name."""
    poll = get_poll_from_name(name)
    if poll is not None:
        return poll.__dict__

    # No matching poll was found.
    abort(404)


@app.route('/api/vote/<name>', methods=['POST'])
def cast_vote(name):
    poll = get_poll_from_name(name)
    if poll is not None:
        poll.cast_vote(request.form.get('option'))
        return poll.__dict__

    # No matching poll was found.
    abort(404)


load_polls()
if __name__ == '__main__':
    app.run()
