from functions import scan_dirs, define_courses_path, only_dirs

courses = scan_dirs(define_courses_path())  # ['Py', 'JS', 'PHP']

for course in courses:
    for section in only_dirs(course):
        for file in only_dirs(section):
            if file.suffix == '.srt' and not file.stem.endswith('_en'):
                file.rename(f'{file.parent}/{file.stem}_en.srt')
