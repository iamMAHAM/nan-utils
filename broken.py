from pathlib import Path
import shutil
import re


# gets an array of Path objects for each folder in courses directory
courses = (Path().cwd() / 'courses').iterdir()
renamed = (Path.cwd()) / 'renamed'
renamed.mkdir(exist_ok=True)

# iterate courses and for each course folder, iterate the files in the folder


def formatFiles():
    for course in courses:
        if (course.is_file()):
            continue
        renamed_course = renamed / course.name
        renamed_course.mkdir(exist_ok=True)
        try:
            coursesList = list(course.iterdir())
            # iterate the files in the course folder
            for i in range(len(coursesList)):
                section = coursesList[i]

                # if section is a file go to next iteration
                if (section.is_file()):
                    continue

                # checks if folder has a rank in the beginning
                sectionRank = re.search(r'^\d+', section.name)
                if (sectionRank is not None):
                    # rank is not none, get the rank and replace it with right rank
                    sectionRank = sectionRank.group(0)
                    section_name = section.name.replace(
                        sectionRank, f'0{i + 1}' if i + 1 < 10 else f'0{i + 1}' if i + 1 < 100 else f'{i + 1}' + ' - ')
                else:
                    # add rank to the section name
                    section_name = (f'0{i + 1}' if i + 1 < 10 else f'0{i + 1}' if i +
                                    1 < 100 else f'{i + 1}') + ' - ' + section.name

                # rename section and create the section folder
                renamed_section = renamed_course / \
                    section_name.replace('.', '-')
                renamed_section.mkdir(exist_ok=True)

                # iterate the files in the section folder
                sectionList = list(section.iterdir())
                for i in range(len(sectionList)):
                    video = sectionList[i]
                    if (video.is_file()):
                        rank_s = re.search(r'^\d+', video.name)
                        if (rank_s is not None):
                            rank = rank_s.group(0)
                            right_rank = f'00{i + 1}' if i + \
                                1 < 10 else f'0{i + 1}' if i + 1 < 100 else f'{i + 1}'

                            # get the video name without the initial rank and replace it with right rank
                            tmp = video.stem.replace(rank, right_rank)

                            # check if the video name has a rank in the beginning and it's the same as right rank
                            new_rank = re.search(r'^\d+', tmp)

                            video_name = tmp.replace(
                                new_rank.group(0), right_rank) if new_rank != right_rank else tmp
                            # rename the video
                            shutil.copy(video, renamed_section /
                                        (video_name.replace('-', '').replace('.', '_') + video.suffix))
                            continue
                        # copy video to new location
                        shutil.copy(video, renamed_section /
                                    (video_name.replace('414 - ', '').replace('-', '').replace('.', '_') + video.suffix))
                    else:
                        # copy folder to new location
                        shutil.copytree(video, renamed_section /
                                        video.name.replace('-', ''))

        except FileExistsError:
            print('file already exists')

        except Exception as e:
            print('an error occured ', e)


if (__name__ == '__main__'):
    formatFiles()
