=== Extended Export ===

    mpvQC allows to customize the export of reports using Jinja (https://jinja.palletsprojects.com/en/3.1.x/)
    by following these steps:

        1. Create a new file in this directory with the .'jinja' extension (e.g: 'MyTemplate.jinja')

        2. Edit the template

        3. Restart mpvQC

        4. The file menu will have a new entry offering to export reports using the new template


=== Template Documentation ===

    In addition to default Jinja expressions, mpvQC adds the following Properties and Filters:


    == Properties ==

              write_date   bool           True if the user enabled the current date & time to be included in reports
                    date   str            Date & time in the user's currently selected language (QLocale.FormatType.LongFormat)

         write_generator   bool           True if the user enabled the generator ('mpvQC' + version) to be included in reports
               generator   str            Name + version of mpvQC (e.g: mpvQC 0.9.0)

        write_video_path   bool           True if the user enabled the path of the video to be included in reports
              video_path   str            Absolute path of the video or the empty string if no video was present

          write_nickname   bool           True if the user enabled the nickname to be included in reports
                nickname   str            Nickname of the person creating the report

                comments   list[object]   List of comment objects with each object having the following properties

                                          time          int    Time in seconds
                                          commentType   str    Comment type in the English language
                                          comment       str    Actual comment


    == Filters ==

                 as_time   Transforms an int into a HH:mm:ss string

                           Example: When iterating over comments, [{{ comment['time'] | as_time }}]
                                    will produce [00:00:00] when time was 0

         as_comment_type   Translates the comment into the user's currently selected language

                           Example: When iterating over comments, [{{ comment['commentType'] | as_comment_type }}]
                                    will produce [Ausdruck] when property commentType was 'Phrasing'


=== Example ===

mpvQC internally uses the following template to save QC documents:

[FILE]
{{ 'date      : ' + date + '\n'       if write_date       else '' -}}
{{ 'generator : ' + generator + '\n'  if write_generator  else '' -}}
{{ 'nick      : ' + nickname + '\n'   if write_nickname   else '' -}}
{{ 'path      : ' + video_path + '\n' if write_video_path else '' -}}

{{ '\n' }}[DATA]
{% for comment in comments -%}
[{{ comment['time'] | as_time }}] [{{ comment['commentType'] | as_comment_type }}] {{ comment['comment'] | trim }}
{% endfor -%}
# total lines: {{ comments | count }}
