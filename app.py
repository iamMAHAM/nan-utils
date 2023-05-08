from pathlib import Path
import shutil
import re


# gets an array of Path objects for each folder in courses directory
courses = (Path().cwd() / 'courses').iterdir()
renamed = (Path.cwd()) / 'renamed'
renamed.mkdir(exist_ok=True)

# iterate courses and for each course folder, iterate the files in the folder
for course in courses:
    if (course.is_file()):
        continue
    renamed_course = renamed / course.name
    renamed_course.mkdir(exist_ok=True)
    try:
        for section in course.iterdir():
            # if section is a file go to next iteration
            if (section.is_file()):
                continue
            renamed_section = renamed_course / section.name
            renamed_section.mkdir(exist_ok=True)

            # iterate the files in the section folder
            for i in range(len(list(section.iterdir()))):
                video = list(section.iterdir())[i]
                if (video.is_file()):
                    rank_s = re.search(r'^\d+', video.name)
                    if (rank_s is not None):
                        rank = rank_s.group(0)
                        # get the video name without the initial rank and replace it with right rank
                        video_name = video.name.replace(
                            rank, f'00{i + 1}' if i + 1 < 10 else f'0{i + 1}' if i + 1 < 100 else f'{i + 1}')

                        # rename the video
                        shutil.copy(video, renamed_section / video_name)
                        continue
                    shutil.copy(video, renamed_section / video.name)
                else:
                    shutil.copytree(video, renamed_section / video.name)

    except FileExistsError:
        print('file already exists')

    except Exception as e:
        print('an error occured ', e)
