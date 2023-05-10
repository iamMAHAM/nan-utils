from pathlib import Path
import shutil
import re


# gets an array of Path objects for each folder in courses directory
courses = (Path().cwd() / 'courses').iterdir()
renamed = (Path.cwd()) / 'renamed'
renamed.mkdir(exist_ok=True)

# iterate courses and for each course folder, iterate the files in the folder
for course in courses:
    if (course.is_file() or 'Django' in course.name):
        continue
    renamed_course = renamed / course.name
    renamed_course.mkdir(exist_ok=True)
    try:
        sections_list = list(filter(lambda x: x.is_dir(), course.iterdir()))

        print(list(map(lambda s: s.name, sections_list)))
        for i in range(len(sections_list)):
            section = sections_list[i]
            # if section is a file go to next iteration
            if (section.is_file()):
                continue

            renamed_section = renamed_course / section.name.replace('.', '-')
            renamed_section.mkdir(exist_ok=True)

            # iterate the files in the section folder
            videos_list = list(section.iterdir())
            for i in range(len(videos_list)):
                video = videos_list[i]
                if (video.is_file()):
                    rank_s = re.search(r'^\d+', video.name)
                    if (rank_s is not None):
                        rank = rank_s.group(0)
                        right_rank = f'00{i + 1}' if i + \
                            1 < 10 else f'0{i + 1}' if i + 1 < 100 else f'{i + 1}'

                        # get the video name without the initial rank and replace it with right rank
                        tmp = video.stem.replace(
                            '414-', '').strip().rstrip().replace(rank, right_rank)

                        # check if the video name has a rank in the beginning and it's the same as right rank
                        new_rank = re.search(r'^\d+', tmp)
                        if (new_rank):
                            video_name = tmp.replace(
                                new_rank.group(0), right_rank) if new_rank.group(0) != right_rank else tmp
                        else:
                            video_name = tmp
                        # rename the video
                        shutil.copy(video, renamed_section /
                                    (video_name.replace('414 - ', '').replace('-', '').replace('.', '') + video.suffix))
                        continue
                    # if rank is none just copy the video
                    shutil.copy(video, renamed_section /
                                video.name.replace('-', ''))
                else:
                    shutil.copytree(video, renamed_section /
                                    video.name.replace('-', ''))

    except FileExistsError:
        print('file already exists')

    except Exception as e:
        print('an error occured ', e)
