import json
import os


def print_keyframe(name, values): 
  result = []
  for key in values:
    result.append(f"{key}:{values[key]}")

  results = ';\n'.join(result) + ';'
  return f"{name} {{\n{results}\n}}"
  

def print_keyframes(name, frames):
  frames_list = []

  for key in frames:
    frames_list.append(print_keyframe(key, frames[key]))
  
  frames_str = '\n'.join(frames_list)

  return f"@keyframes {name} {{ \n {frames_str} \n }}"

def print_animation(name, animation):
  result = []
  for key in animation:
    result.append(f"{key}:{animation[key]}")
  results = ';\n'.join(result) + ';'
  return f"#{name} {{\n{results}\n}}"

def print_path(stroke, fill="lightgray"):
  return f"<path d=\"{stroke}\" fill=\"{fill}\"></path>"

def print_clip_path(clip, index):
  return f"<path id=\"animation-{index}\" clip-path=\"url(#{clip['id']})\" d=\"{clip['stroke']}\" stroke-dasharray=\"{clip["stroke-dasharray"]}\" stroke-linecap=\"round\" fill=\"none\"/>"

def make_svg(clues):
  keyframes = clues['keyframes']
  keyframes_list = []

  for key in keyframes:
    keyframe = keyframes[key]
    keyframes_list.append(print_keyframes(key, keyframe))


  animations = clues['animations']
  animations_list = []
  for key in animations:
    animation = animations[key]
    animations_list.append(print_animation(key, animation))


  path_list = []
  strokes = clues['strokes']
  for stroke in strokes:
    path_list.append(print_path(stroke))

  clip_path_path = []
  for index, stroke in enumerate(strokes):
    clip_path_path.append(f"<clipPath id=\"clip-{index}\"><path d=\"{stroke}\"></path></clipPath>")
  
  
  clip_list = []
  for index,clip in enumerate(clues['clips']):
    clip_list.append(print_clip_path(clip, index))

  return f"""
    <svg version=\"1.1\" viewBox=\"0 0 1024 1024\" xmlns=\"http://www.w3.org/2000/svg\">
      <g stroke=\"lightgray\" stroke-dasharray=\"1,1\" stroke-width=\"1\" transform=\"scale(4, 4)\">
        <line x1=\"0\" y1=\"0\" x2=\"256\" y2=\"256\"></line>
        <line x1=\"256\" y1=\"0\" x2=\"0\" y2=\"256\"></line>
        <line x1=\"128\" y1=\"0\" x2=\"128\" y2=\"256\"></line>
        <line x1=\"0\" y1=\"128\" x2=\"256\" y2=\"128\"></line>
      </g>
      <g transform=\"scale(1, -1) translate(0, -900)\">
        <style type=\"text/css\">
          {'\n'.join(keyframes_list)}
          
          {'\n'.join(animations_list)}
        </style>
          {'\n'.join(path_list)}

          {'\n'.join(clip_path_path)}

          {'\n'.join(clip_list)}
      </g>
    </svg>
    """



if __name__ == '__main__':
  with open(os.path.join(os.path.dirname(__file__), '../data/11904.json')) as file:
    clues = json.loads(file.read())
    svg_str = make_svg(clues)
    with open(os.path.join(os.path.dirname(__file__), '../output/11904.svg'), 'w') as svg_file:
      svg_file.write(svg_str)