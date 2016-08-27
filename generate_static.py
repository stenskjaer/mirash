#!/usr/bin/env python

from jinja2 import Environment, FileSystemLoader
import os
import session_data as data

PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, 'templates')),
    trim_blocks=True,
    lstrip_blocks = True,
)
 
 
def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)


def session_name(session_number):
    """Convert session numbers to plain English
    """
    if session_number is 1:
        return 'morning'
    elif session_number is 2:
        return 'afternoon'
    else:
        return 'session' + session_number


def generate_player_statics():
    for item in data.session_dict:
        context = {
            'title': data.session_dict[item]['date'] + ', ' + session_name(data.session_dict[item]['session']),
            'pub_date': data.session_dict[item]['pub_date'],
            'chapters': data.session_dict[item]['chapters'],
            'duration': data.session_dict[item]['duration'],
            'session': item,
            'description': data.session_dict[item]['description'],
            'filesize': os.path.getsize('static/recordings/' + item + '.mp3'),
        }
        with open('pages/recordings/inject/' + item + '.html', 'w') as f:
            html = render_template('player.html', context)
            f.write(html)


def generate_recording_pages():
    for item in data.session_dict:
        context = {
            'session': item,
        }
        with open('pages/recordings/' + item + '.html', 'w') as f:
            html = render_template('recording.html', context)
            f.write(html)


def generate_song_index():
    """Return a list of nav.Items with deep link references to each song. 
    """
    session_dictionary = data.session_dict
    title_info = []

    for session in sorted(data.session_dict):
        for recording in session_dictionary[session]['chapters']:
            # First, try adding session data with song number
            try:
                title_info.append(
                    {
                        'session': session,
                        'number': recording[1][1].split('.')[0],
                        'type': recording[1][1].split(',')[-1],
                        'title': recording[1][1],
                        'start': recording[0][1],
                        'sort': recording[2][1],
                        'date': session_dictionary[session]['date'] +
                        ', ' + session_name(session_dictionary[session]['session']),
                    }
                )
            except IndexError:
                pass

            # Then, try adding session data with page info
            try:
                title_info.append(
                    {
                        'session': session,
                        'title': '{0}'.format(
                            ','.join(recording[1][1].split(',')[:-1]) +
                            ', written'
                        ),
                        'start': recording[0][1],
                        'sort': recording[2][1],
                        'page': recording[3][1],
                        'date': session_dictionary[session]['date'] +
                        ', ' + session_name(session_dictionary[session]['session']),
                    }
                )
            except IndexError:
                pass

    sorted_context = sorted(title_info, key=lambda x: x['sort'])
    with open('pages/song-index.html', 'w') as f:
        html = render_template('index-generator.html', {'context':sorted_context})
        f.write(html)



def main():
    generate_player_statics()
    generate_recording_pages()
    generate_song_index()

if __name__ == "__main__":
    main()
