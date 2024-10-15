# import re

# def extract_mark_positions_in_plain_text(plain_text, markup_text):
#     marks = []
#     current_pos = 0

#     # Regex to find all <mark>...</mark> patterns
#     for match in re.finditer(r'(<mark[^>]*>)(.*?)(</mark>)', markup_text):
#         full_mark_tag = match.group(0)  # Get the entire <mark>...</mark> tag
#         marked_text = match.group(2)     # Extract the text inside the <mark> tags

#         # Search for the marked text in the plain text, starting from the last found position
#         start_in_plain = plain_text.find(marked_text, current_pos)
        
#         # If found, calculate the end position
#         if start_in_plain != -1:
#             end_in_plain = start_in_plain + len(marked_text)
#             marks.append((start_in_plain, end_in_plain, full_mark_tag))

#             # Update the current position to continue searching after this point
#             current_pos = end_in_plain

#     return marks

# # Example inputs
# plain_text = '''One sunny morning my mum and I were cleaning out our grandfather’s shed, then my mum got a call from work and needed to go, she said to me “can you please stay and clean the shed?” "yes mum” I said “do you want a friend to come over?” she said “ok I’ll go call Hannah to see if she can come over” So my mum left and Hannah came over, we were cleaning until Hannah said “What’s in this little red box?” I said “Open it and find out.” “OK” said Hannah so Hannah opened the box all of a sudden we had gold and silver everywhere! And we ate a sandwich. But then we heard a big “BANG” we stopped and looked at each other then out of nowhere came a big bully and the bully said “Give me your gold and silver now!” “No” said Hannah “it’s ours and you’re not having it so go away!” But the bully didn’t like that at all. so she took it all and ran off “after her!” said Hannah so we ran as fast as we could, and Hannah opened the box again and then we had jet packs! Hannah said this box is magic! "Cool" I said then we caught the bully and got our gold and silver back then when we got home I opened the box and everything was back to normal.'''


# markup_text_1 = '''One sunny morning my <mark data="32,*">mum</mark> and I were cleaning out our grandfatherÆs shed, then my <mark data="36,*">mum</mark> got a call from work and needed to go, she said to me ôcan you please stay and clean the shed?ö ôyes <mark data="32,*">mum</mark>ö I said ôdo you want a friend to come over?ö she said ôok IÆll go call <mark data="32,*">Hannah</mark> to see if she can come overö So my <mark data="36,*">mum</mark> left and <mark data="36,*">hannah</mark> came over, we were cleaning until <mark data="36,*">hannah</mark> said ôWhatÆs in this little red box?ö I said ôOpen it and find out.ö ôOKö said <mark data="36,*">hannah</mark> so <mark data="36,*">hannah</mark> opened the box all of a sudden we had gold and silver everywhere! And we ate a sandwich. But then we heard a big ôBANGö we stopped and looked at each other then out of nowhere came a big bully and the <mark data="32,*">bully</mark> said ôGive me your gold and silver now!ö ôNoö said <mark data="36,*">hannah</mark> ôitÆs ours and youÆre not having it so go away!ö But the <mark data="32,*">bully</mark> didnÆt like that at all. so she took it all and ran off ôafter her!ö said <mark data="36,*">hannah</mark> so we ran as fast as we could, and <mark data="36,*">hannah</mark> opened the box again and then we had jet packs! <mark data="36,*">Hannah</mark> said this box is magic!ô Coolö I said then we caught the <mark data="32,*">bully</mark> and got our gold and silver back then when we got home I opened the box and everything was back to normal.'''
# markup_text_2 = '''One sunny moring my mum and <mark data="33,*">I</mark> were cleaning out our grandfatherÆs shed, then my mum got a call from work and needed to go, <mark data="33,*">she</mark> said to me ôcan <mark data="33,*">you</mark> please stay and clean the shed?ö ôyes mumö <mark data="33,*">I</mark> said ôdo <mark data="33,*">you</mark> want a friend to come over?ö <mark data="33,*">she</mark> said ôok <mark data="33,*">I</mark>Æll go call Hannah to see if <mark data="33,*">she</mark> can come overö So my mum left and <mark data="33,*">Hannah</mark> came over, <mark data="33,*">we</mark> were cleaning until <mark data="33,*">Hannah</mark> said ôWhatÆs in this little red box?ö <mark data="33,*">I</mark> said ôOpen <mark data="33,*">it</mark> and find out.ö ôOKö said <mark data="33,*">Hannah</mark> so <mark data="33,*">Hannah</mark> opened the box all of a sudden <mark data="33,*">we</mark> had gold and silver everywhere! And <mark data="33,*">we</mark> ate a sandwich. But then <mark data="33,*">we</mark> heard a big ôBANGö <mark data="33,*">we</mark> stopped and looked at each other then out of nowhere came a big bully and the bully said ôGive me your gold and silver now!ö ôNoö said <mark data="33,*">Hannah</mark> ô<mark data="37,*">it</mark>Æs ours and <mark data="33,*">you</mark>Ære not having <mark data="37,*">it</mark> so go away!ö But the bully didnÆt like that at all. so <mark data="33,*">she</mark> took <mark data="37,*">it</mark> all and ran off ôafter <mark data="33,*">her</mark>!ö said <mark data="33,*">Hannah</mark> so <mark data="33,*">we</mark> ran as fast as <mark data="33,*">we</mark> could, and <mark data="33,*">Hannah</mark> opened the box again and then <mark data="33,*">we</mark> had jet packs! <mark data="33,*">Hannah</mark> said this box is magic!ô Coolö <mark data="33,*">I</mark> said then <mark data="33,*">we</mark> caught the bully and got our gold and silver back then when <mark data="33,*">we</mark> got home <mark data="33,*">I</mark> opened the box and everything was back to normal.'''
# markup_text_3 = '''One sunny morning my mum and I were cleaning out our grandfatherÆs shed, <mark data="29,2">then</mark> my mum got a call from work and needed to go, she said to me ôcan you please stay and clean the shed?ö ôyes mumö I said ôdo you want a friend to come over?ö she said ôok IÆll go call Hannah to see if she can come overö So my mum left and Hannah came over, we were cleaning <mark data="30,*">until</mark> Hannah said ôWhatÆs in this little red box?ö I said ôOpen it and find out.ö ôOKö said Hannah <mark data="29,2">so</mark> Hannah opened the box <mark data="29,2">all of a sudden</mark> we had gold and silver everywhere! And we ate a sandwich. <mark data="29,2">But then</mark> we heard a big ôBANGö we stopped and looked at each other <mark data="29,2">then</mark> out of nowhere came a big bully and the bully said ôGive me your gold and silver now!ö ôNoö said Hannah ôitÆs ours and youÆre not having it <mark data="30,*">so</mark> go away!ö <mark data="30,*">But</mark> the bully didnÆt like that at all. <mark data="30,*">so</mark> she took it all and ran off ôafter her!ö said Hannah <mark data="29,2">so</mark> we ran as fast as we could, and Hannah opened the box again <mark data="29,2">and then</mark> we had jet packs! Hannah said this box is magic!ô Coolö I said <mark data="29,2">then</mark> we caught the bully and got our gold and silver back <mark data="30,*">then</mark> when we got home I opened the box and everything was back to normal.'''

# # Extract positions of text inside <mark> tags relative to plain text
# positions = extract_mark_positions_in_plain_text(plain_text, markup_text_1)

# # Output the positions
# print("Positions in plain text:", positions)

# # Extract positions of text inside <mark> tags relative to plain text
# positions = extract_mark_positions_in_plain_text(plain_text, markup_text_2)

# # Output the positions
# print("Positions in plain text:", positions)

# # Extract positions of text inside <mark> tags relative to plain text
# positions = extract_mark_positions_in_plain_text(plain_text, markup_text_3)

# # Output the positions
# print("Positions in plain text:", positions)

# Original text with markup
# marked_positions = [
#     (21, 24, '<mark data="32,*">mum</mark>'), 
#     (81, 84, '<mark data="36,*">mum</mark>'), 
#     (186, 189, '<mark data="32,*">mum</mark>'), 
#     (261, 267, '<mark data="32,*">Hannah</mark>'), 
#     (303, 306, '<mark data="36,*">mum</mark>'), 
#     (647, 652, '<mark data="32,*">bully</mark>'), 
#     (661, 666, '<mark data="32,*">bully</mark>'), 
#     (718, 724, '<mark data="36,*">Hannah</mark>'), 
#     (782, 787, '<mark data="32,*">bully</mark>'),
#     (29, 30, '<mark data="33,*">I</mark>'), 
#     (67, 70, '<mark data="33,*">she</mark>'), 
#     (144, 147, '<mark data="33,*">you</mark>'), 
#     (191, 192, '<mark data="33,*">I</mark>'), 
#     (202, 205, '<mark data="33,*">you</mark>'), 
#     (235, 238, '<mark data="33,*">she</mark>'), 
#     (248, 249, '<mark data="33,*">I</mark>'), 
#     (278, 281, '<mark data="33,*">she</mark>'), 
#     (316, 322, '<mark data="33,*">Hannah</mark>'), 
#     (334, 336, '<mark data="33,*">we</mark>'), 
#     (357, 363, '<mark data="33,*">Hannah</mark>'), 
#     (402, 403, '<mark data="33,*">I</mark>'), 
#     (415, 417, '<mark data="33,*">it</mark>'), 
#     (443, 449, '<mark data="33,*">Hannah</mark>'), 
#     (453, 459, '<mark data="33,*">Hannah</mark>'), 
#     (491, 493, '<mark data="33,*">we</mark>'), 
#     (530, 532, '<mark data="33,*">we</mark>'), 
#     (558, 560, '<mark data="33,*">we</mark>'), 
#     (580, 582, '<mark data="33,*">we</mark>'), 
#     (718, 724, '<mark data="33,*">Hannah</mark>'), 
#     (726, 728, '<mark data="37,*">it</mark>'), 
#     (740, 743, '<mark data="33,*">you</mark>'), 
#     (758, 760, '<mark data="37,*">it</mark>'), 
#     (816, 819, '<mark data="33,*">she</mark>'), 
#     (825, 827, '<mark data="37,*">it</mark>'), 
#     (851, 854, '<mark data="33,*">her</mark>'), 
#     (862, 868, '<mark data="33,*">Hannah</mark>'), 
#     (872, 874, '<mark data="33,*">we</mark>'), 
#     (890, 892, '<mark data="33,*">we</mark>'), 
#     (904, 910, '<mark data="33,*">Hannah</mark>'), 
#     (941, 943, '<mark data="33,*">we</mark>'), 
#     (959, 965, '<mark data="33,*">Hannah</mark>'), 
#     (997, 998, '<mark data="33,*">I</mark>'), 
#     (1009, 1011, '<mark data="33,*">we</mark>'), 
#     (1072, 1074, '<mark data="33,*">we</mark>'), 
#     (1084, 1085, '<mark data="33,*">I</mark>'), 
#     (73, 77, '<mark data="29,2">then</mark>'), 
#     (351, 356, '<mark data="30,*">until</mark>'), 
#     (450, 452, '<mark data="29,2">so</mark>'), 
#     (475, 490, '<mark data="29,2">all of a sudden</mark>'), 
#     (549, 557, '<mark data="29,2">But then</mark>'), 
#     (616, 620, '<mark data="29,2">then</mark>'), 
#     (761, 763, '<mark data="30,*">so</mark>'), 
#     (774, 777, '<mark data="30,*">But</mark>'), 
#     (813, 815, '<mark data="30,*">so</mark>'), 
#     (869, 871, '<mark data="29,2">so</mark>'), 
#     (932, 940, '<mark data="29,2">and then</mark>'), 
#     (1004, 1008, '<mark data="29,2">then</mark>'), 
#     (1062, 1066, '<mark data="30,*">then</mark>')
# ]

# # Original text
# original_text = '''One sunny morning my mum and I were cleaning out our grandfather’s shed, then my mum got a call from work and needed to go, she said to me “can you please stay and clean the shed?” "yes mum” I said “do you want a friend to come over?” she said “ok I’ll go call Hannah to see if she can come over” So my mum left and Hannah came over, we were cleaning until Hannah said “What’s in this little red box?” I said “Open it and find out.” “OK” said Hannah so Hannah opened the box all of a sudden we had gold and silver everywhere! And we ate a sandwich. But then we heard a big “BANG” we stopped and looked at each other then out of nowhere came a big bully and the bully said “Give me your gold and silver now!” “No” said Hannah “it’s ours and you’re not having it so go away!” But the bully didn’t like that at all. so she took it all and ran off “after her!” said Hannah so we ran as fast as we could, and Hannah opened the box again and then we had jet packs! Hannah said this box is magic! "Cool" I said then we caught the bully and got our gold and silver back then when we got home I opened the box and everything was back to normal.'''

# # Function to insert marks in original text
# def mark_text(original, positions):
#     marked_text = original
#     marked_indices = set()  # To keep track of already marked positions

#     for start, end, mark in positions:
#         # Check if this position has already been marked
#         if not any(start < marked_start < end or start < marked_end < end for marked_start, marked_end in marked_indices):
#             # Add the marked range to the set
#             marked_indices.add((start, end))
#             # Insert the mark in the original text
#             marked_text = marked_text[:start] + mark + marked_text[start:end] + '</mark>' + marked_text[end:]

#     return marked_text

# # Generate the marked text
# fixed_marked_text = mark_text(original_text, marked_positions)

# # Print the result
# print(fixed_marked_text)

from textprocessor.task_runners import PipelineTaskRunner
import textprocessor.postprocess_nlp_llm as pnl
from textprocessor.data_models import ComponentData, Flag

pp_result =  [[{'nlp_annotated': [{'comp_id': 1, 'start': 260, 'end': 266, 'flag': 11}, {'comp_id': 1, 'start': 442, 'end': 448, 'flag': 11}, {'comp_id': 1, 'start': 452, 'end': 458, 'flag': 11}, {'comp_id': 1, 'start': 861, 'end': 867, 'flag': 11}, {'comp_id': 1, 'start': 903, 'end': 909, 'flag': 11}, {'comp_id': 1, 'start': 958, 'end': 964, 'flag': 11}, {'comp_id': 5, 'start': 70, 'end': 71, 'flag': 10}, {'comp_id': 5, 'start': 121, 'end': 122, 'flag': 10}, {'comp_id': 10, 'start': 255, 'end': 259, 'flag': 11}, {'comp_id': 10, 'start': 270, 'end': 273, 'flag': 11}, {'comp_id': 10, 'start': 306, 'end': 310, 'flag': 11}, {'comp_id': 5, 'start': 331, 'end': 332, 'flag': 10}, {'comp_id': 10, 'start': 363, 'end': 367, 'flag': 11}, {'comp_id': 10, 'start': 493, 'end': 496, 'flag': 11}, {'comp_id': 10, 'start': 582, 'end': 589, 'flag': 11}, {'comp_id': 10, 'start': 892, 'end': 897, 'flag': 11}, {'comp_id': 5, 'start': 897, 'end': 898, 'flag': 10}, {'comp_id': 10, 'start': 1074, 'end': 1077, 'flag': 11}, {'comp_id': 4, 'start': 177, 'end': 178, 'flag': 10}, {'comp_id': 4, 'start': 231, 'end': 232, 'flag': 10}, {'comp_id': 4, 'start': 294, 'end': 295, 'flag': 11}, {'comp_id': 4, 'start': 398, 'end': 399, 'flag': 10}, {'comp_id': 4, 'start': 429, 'end': 430, 'flag': 10}, {'comp_id': 4, 'start': 523, 'end': 524, 'flag': 10}, {'comp_id': 4, 'start': 546, 'end': 547, 'flag': 10}, {'comp_id': 4, 'start': 704, 'end': 705, 'flag': 10}, {'comp_id': 4, 'start': 733, 'end': 734, 'flag': 11}, {'comp_id': 4, 'start': 770, 'end': 771, 'flag': 10}, {'comp_id': 4, 'start': 810, 'end': 811, 'flag': 10}, {'comp_id': 4, 'start': 929, 'end': 930, 'flag': 11}, {'comp_id': 4, 'start': 956, 'end': 957, 'flag': 10}, {'comp_id': 4, 'start': 988, 'end': 989, 'flag': 11}, {'comp_id': 4, 'start': 1133, 'end': 1134, 'flag': 10}, {'comp_id': 13, 'start': 178, 'end': 179, 'flag': 11}, {'comp_id': 13, 'start': 232, 'end': 233, 'flag': 11}, {'comp_id': 13, 'start': 294, 'end': 295, 'flag': 11}, {'comp_id': 13, 'start': 399, 'end': 400, 'flag': 11}, {'comp_id': 13, 'start': 430, 'end': 431, 'flag': 11}, {'comp_id': 13, 'start': 523, 'end': 524, 'flag': 10}, {'comp_id': 13, 'start': 546, 'end': 547, 'flag': 10}, {'comp_id': 13, 'start': 705, 'end': 706, 'flag': 11}, {'comp_id': 13, 'start': 733, 'end': 734, 'flag': 11}, {'comp_id': 13, 'start': 771, 'end': 772, 'flag': 11}, {'comp_id': 13, 'start': 810, 'end': 811, 'flag': 10}, {'comp_id': 13, 'start': 929, 'end': 930, 'flag': 11}, {'comp_id': 13, 'start': 956, 'end': 957, 'flag': 10}, {'comp_id': 13, 'start': 988, 'end': 989, 'flag': 11}, {'comp_id': 13, 'start': 1133, 'end': 1134, 'flag': 10}, {'comp_id': 11, 'start': 350, 'end': 355, 'flag': None}, {'comp_id': 11, 'start': 886, 'end': 888, 'flag': None}]}]]
text = '''One sunny moring my mum and I were cleaning out our grandfather’s shed, then my mum got a call from work and needed to go, she said to me “can you please stay and clean the shed?” “yes mum” I said “do you want a friend to come over?” she said “ok I’ll go call Hannah to see if she can come over” So my mum left and hannah came over, we were cleaning until hannah said “What’s in this little red box?” I said “Open it and find out.” “OK” said hannah so hannah opened the box all of a sudden we had gold and silver everywhere! And we ate a sandwich. But then we heard a big “BANG” we stopped and looked at each other then out of nowhere came a big bully and the bully said “Give me your gold and silver now!” “No” said hannah “it’s ours and you’re not having it so go away!” But the bully didn’t like that at all. so she took it all and ran off “after her!” said hannah so we ran as fast as we could, and hannah opened the box again and then we had jet packs! Hannah said this box is magic!“ Cool” I said then we caught the bully and got our gold and silver back then when we got home I opened the box and everything was back to normal.'''
metadata={'components': {1: ComponentData(name='capitalise proper noun', markup_id=1), 2: ComponentData(name='capitalise key event', markup_id=1), 3: ComponentData(name='possessive apostrophie', markup_id=1), 4: ComponentData(name='sentence boundary punct.', markup_id=1), 5: ComponentData(name='commas - lists', markup_id=1), 6: ComponentData(name='commas - dates', markup_id=1), 7: ComponentData(name='commas - pauses', markup_id=1), 8: ComponentData(name='commas - quotes', markup_id=1), 9: ComponentData(name='quotes for dialogue', markup_id=1), 10: ComponentData(name='commas - separate clauses', markup_id=1), 11: ComponentData(name='subordinating clause', markup_id=1), 12: ComponentData(name='complex dialogue', markup_id=1), 13: ComponentData(name='simple punctuation', markup_id=1), 14: ComponentData(name='complex punctuation', markup_id=1)}, 'flags': {1: Flag(colour='black', characters='CC'), 2: Flag(colour='black', characters='TS'), 3: Flag(colour='black', characters='E'), 4: Flag(colour='black', characters='C'), 5: Flag(colour='black', characters='CE'), 6: Flag(colour='black', characters='IA'), 7: Flag(colour='black', characters='I'), 8: Flag(colour='black', characters='C'), 9: Flag(colour='black', characters='CJ'), 10: Flag(colour='green', characters=None), 11: Flag(colour='red', characters=None)}}


 # Post process NLP/LLM
runner = PipelineTaskRunner().input(pp_result)
runner.add_task(pnl.preprocess_result)
runner.add_task(pnl.process_llm_annotated, text)
runner.add_task(pnl.combine_llm_nlp)
runner.add_task(pnl.remove_overlaps)
runner.add_task(pnl.markup_annotated, text, metadata)

pl_result = runner.run_all()

print(pl_result)