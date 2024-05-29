import json
import os

import tinycss2
# import xml.etree.ElementTree as ET
from lxml import etree as ET


def extract_from_block(block):
  blockStr = tinycss2.serialize(block)
  declarations = filter(lambda d: d.type == 'declaration', tinycss2.parse_blocks_contents(blockStr))

  filter_non_whitespace = lambda d: d.type != 'whitespace'
  values = {}
  for d in declarations:
    values[d.name] = list(map(lambda c: c.value, filter(filter_non_whitespace, d.value)))[0]
  return values
  

def extract_animation_clues(filepath):
  with open(filepath) as file:
    tree = ET.parse(file)
    root = tree.getroot()

    # Extract tags
    nodes = [elem for elem in root.iter()]

    i = -1
    clips = []
    cssSnippets = []
    strokes = []
    for node in nodes:
      tagName = node.tag.split('}')[1]
      if tagName == 'style':
        cssSnippets.append(node.text)
      elif tagName == 'clipPath':
        i = i + 1
        clips.append({'id': node.attrib['id'].replace('make-me-a-hanzi-', '')})
      elif tagName == 'path':
        if 'clip-path' in node.attrib:
          clips[i]['stroke'] = node.attrib['d']
          clips[i]['stroke-dasharray'] = node.attrib['stroke-dasharray']
        else:
          parent = node.getparent()
          if parent is not None and 'clipPath' in parent.tag:
            continue
          strokes.append(node.attrib['d'])

    keyframes = {}
    animations = {}

    for snippet in cssSnippets:
      rules = tinycss2.parse_stylesheet(snippet)
      for rule in rules:
        if rule.type == 'whitespace':
          continue
        elif rule.type == 'at-rule' and rule.at_keyword == 'keyframes':
          current = ''
          keyframe = {}
          for component in rule.content:
            if component.type == 'whitespace':
              continue
            elif component.type == 'ident':
              keyframe[component.value] = {}
              current = component.value
            elif component.type == 'percentage':
              keyframe[f"{component.value}%"] = {}
              current = f"{component.value}%"
            elif component.type == '{} block':
              block = extract_from_block(component.content)
              keyframe[current] = block
            else:
              print(f"unknown tag: {component.type}")
          keyframes[rule.prelude[1].value] = keyframe
        else:
          id = rule.prelude[0].value.replace('make-me-a-hanzi-', '')
          block = extract_from_block(rule.content)
          animations[id] = block
      
    clues = {'keyframes': keyframes, 'animations': animations, 'clips': clips, 'strokes': strokes}
    return clues

if __name__ == '__main__':
  clues = extract_animation_clues(os.path.join(os.path.dirname(__file__), '../data/11904.svg'))
  with open(os.path.join(os.path.dirname(__file__), '../data/11904.json'), 'w') as file:
    file.write(json.dumps(clues))