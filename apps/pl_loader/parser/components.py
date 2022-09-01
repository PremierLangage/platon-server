#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  source.py
#
#  Copyright 2019 Cisse Mamadou [mciissee@gmail.com]

import importlib
import inspect
import json
import random
import sys
import uuid



def components_source():
    """
    Used by playexo to retrieve the place this file
    on the sandbox before a build
    """
    
    mod = sys.modules[__name__]
    return inspect.getsource(mod)


# MAP OF CURRENTS COMPONENTS WHERE KEY
# IS THE NAME OF THE COMPONENT AND VALUE
# THE SELECTOR OF THE COMPONENT
SELECTORS = {
    "AutomatonDrawer": "wc-automaton-drawer",
    "AutomatonEditor": "wc-automaton-editor",
    "CheckboxGroup":   "wc-checkbox-group",
    "CodeEditor":      "wc-code-editor",
    "DragDrop":        "wc-drag-drop",
    "GraphDrawer":     "wc-graph-drawer",
    "Input":           "wc-input",
    "MatchList":       "wc-match-list",
    "MathDrawer":      "wc-math-drawer",
    "MathInput":       "wc-math-input",
    "MathMatrix":      "wc-math-matrix",
    "RadioGroup":      "wc-radio-group",
    "SortList":        "wc-sort-list",
    "Text":            "wc-text",
    "TransfertList":   "wc-transfert-list"
}



class Component:
    """
        Base class of the components.
    """
    
    
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        
        if getattr(self, 'cid', '') == '':
            self.cid = str(uuid.uuid4())
    
    
    def __str__(self):
        return str(vars(self))
    
    
    @staticmethod
    def deserialize(target, data):
        """
        Transforms `target` into the instance of a class extending `Component`
        and initializes its fields with the given dict `data`.

        - If `target` is already an instance of `Component` values of
        `data` will be copied into it. (always true if deserialized during grade)

        - if 'target' is a dict (always true during build) and `decorator` key is in it,
        target will be instancied as an instance of decorator retrieved from the sandbox.

        - If none of the case above are not respected, the method will creates
        and instance of the type depending of `selector` key of `data`.
        """
        if isinstance(target, Component):
            for k, v in data.items():
                setattr(target, k, v)
            return target
        
        decorator = None
        
        if isinstance(target, dict):
            decorator = data.get('decorator')
        
        if decorator:
            module = importlib.import_module(decorator.lower())
            return getattr(module, decorator)(**data)
        
        selector = data.get('selector')
        if not selector:
            msg = 'selector property is required for components'
            raise Exception(msg)
        for k in SELECTORS:
            if SELECTORS[k] == selector:
                cls = globals().get(k)
                if not cls:
                    break
                return cls(**data)
        
        return Component(**data)
    
    
    @staticmethod
    def sync_context(context):
        context['Component'] = Component
        for k in SELECTORS:
            context[k] = globals()[k]
        
        # tranform dict with cid properties to a component
        for k, v in context.items():
            if isinstance(v, dict) and 'cid' in v:
                context[k] = Component.deserialize(v, v)
        
        # sync answers with context in grader
        answers = None
        for arg in sys.argv:
            if arg == 'answers.json':
                with open(arg, "r") as f:
                    answers = json.load(f)
                    break
        
        copy = dict(context)
        if answers:
            for k, v in answers.items():
                if isinstance(v, dict) and "cid" in v:
                    for k2, v2 in copy.items():
                        if isinstance(v2, Component) and v2.cid == v["cid"]:
                            context[k2] = Component.deserialize(v2, v)
    
    
    @staticmethod
    def from_context(context):
        components = {}
        for k, v in context.items():
            if isinstance(v, dict) and 'cid' in v:
                components[k] = {
                    e: v[e] for e in v if not e.startswith('_')
                }
        return components



class SortList(Component):
    """
    Custom class for SortList component.
    """
    
    
    def __init__(self, **kwargs):
        self._answer = []
        super().__init__(**kwargs)
        self.selector = 'wc-sort-list'
    
    
    def remind(self):
        """
        Saves the current ordering of the items
        to provides auto correction when self.auto_grade()
        will be called.

        The method stores the id properties of the items
        in a list and compares it with the list retrieved
        during evaluation.

        Then it will randomize the items
        """
        
        # since self._answer starts with '_'
        # it will be hidden to the student
        
        self._answer = []
        for e in self.items:
            self._answer.append(e['id'])
        
        random.shuffle(self.items)
    
    
    def parse_string(self, separator="\n"):
        """
        Assumes that current type of self.items is str
        and initializes items to the JSON format required
        by the component in JS.

        The method will split the items by using the argument separator.
        """
        items = self.items.split(separator)
        self.items = []
        for e in items:
            if e.strip():
                self.items.append({
                    "id":      str(uuid.uuid4()),
                    "content": e,
                })
    
    
    def auto_grade(self):
        """
        Provides an grade according to the answer of a student using the list
        saved during the last call to self.remind()
        """
        
        score = 0
        if len(self._answer) != len(self.items):
            for e in self.items:
                e["css"] = "error-state anim-fade"
            return 0
        
        for i, e in enumerate(self._answer):
            self.items[i]['css'] = 'success-state anim-fade'
            score += 1
            if self.items[i]['id'] != e:
                self.items[i]['css'] = 'error-state anim-fade'
                score -= 1
        
        return score / len(self._answer)



class AutomatonEditor(Component):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selector = 'wc-automaton-editor'



class AutomatonDrawer(Component):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selector = 'wc-automaton-drawer'



class CheckboxGroup(Component):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selector = 'wc-checkbox-group'



class CodeEditor(Component):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selector = 'wc-code-editor'



class DragDrop(Component):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selector = 'wc-drag-drop'



class GraphDrawer(Component):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selector = 'wc-graph-drawer'



class Input(Component):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selector = 'wc-input'



class MatchList(Component):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selector = 'wc-match-list'



class MathDrawer(Component):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selector = 'wc-math-drawer'



class MathInput(Component):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selector = 'wc-math-input'



class MathMatrix(Component):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selector = 'wc-math-matrix'



class RadioGroup(Component):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selector = 'wc-radio-group'



class Text(Component):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selector = 'wc-text'



class TransfertList(Component):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selector = 'wc-transfert-list'
