from functions import define_courses_path, get_folder_files, scan_dirs, copy_files, sort_by_rank
from colorama import init, Fore as F
from pathlib import Path
import re

init(autoreset=True)
all_courses = scan_dirs(define_courses_path())  # ['Py', 'JS', 'PHP']
renamed = (Path.cwd()) / 'renamed'
renamed.mkdir(exist_ok=True)
# regex pour extraire le numero de la section
regex = r'[a-zA-Z].*$'

# pour chaque speciality_course dans all_courses
try:
    for speciality_courses in all_courses:
        print(F.MAGENTA + f'Processing {speciality_courses.name} Courses...')
        new_spec_course_folder = renamed / speciality_courses.name
        new_spec_course_folder.mkdir(exist_ok=True)

        # pour chaque course dans speciality_courses
        courses = scan_dirs(speciality_courses)  # ['react', 'vue', 'angular']
        for course in courses:
            print(F.LIGHTCYAN_EX +
                  f'Processing {course.name}  rank {courses.index(course) + 1}/{len(courses)}...')
            new_course_folder = new_spec_course_folder / course.name
            new_course_folder.mkdir(exist_ok=True)

            # pour chaque section dans course
            # ['section1', 'section2', 'section3']
            sections = sort_by_rank(scan_dirs(course))
            for i in range(len(sections)):
                section = sections[i]

                new_section_name = section.name
                # trouver le nouveau nom de la section en utilisant
                # le numero de la section et en remplaçant tout avant
                # la premiere lettre par le numero de la section
                match = re.search(regex, section.name)
                if match:
                    new_section_name = (
                        f'0{i}' if i < 10 else f'{i}') + ' - ' + match.group()

                new_section_folder = new_course_folder / new_section_name
                new_section_folder.mkdir(exist_ok=True)
                files = sort_by_rank(get_folder_files(section))
                # print(files)

                # pour chaque fichier dans section
                for i in range(len(files)):
                    file = files[i]

                    new_file_name = file.name
                    match = re.search(regex, file.stem.replace('.', ''))
                    if match:
                        new_file_name = (
                            f'00{i}' if i < 10 else f'0{i}' if i <
                            100 else f'{i}') + ' - ' + match.group() + file.suffix

                    # copier le fichier dans le nouveau dossier avec son nouveau nom
                    copy_files(file, new_section_folder / new_file_name)
except Exception as e:
    print(F.RED + 'An error occured', e)

print(F.GREEN + 'Done ! 🎉')
