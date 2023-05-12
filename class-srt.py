from functions import scan_dirs, define_courses_path

courses = scan_dirs(define_courses_path())  # ['Py', 'JS', 'PHP']

for course in courses:
    for section in course.iterdir():
        for file in section.iterdir():
            if file.suffix == '.srt' and not file.stem.endswith('_en'):
                print(file.stem, file.suffix)
                file.rename(f'{file.parent}/{file.stem}_en.srt')
