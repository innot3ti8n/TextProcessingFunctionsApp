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
marked_positions = [
    (21, 24, '<mark data="32,*">mum</mark>'), 
    (81, 84, '<mark data="36,*">mum</mark>'), 
    (186, 189, '<mark data="32,*">mum</mark>'), 
    (261, 267, '<mark data="32,*">Hannah</mark>'), 
    (303, 306, '<mark data="36,*">mum</mark>'), 
    (647, 652, '<mark data="32,*">bully</mark>'), 
    (661, 666, '<mark data="32,*">bully</mark>'), 
    (718, 724, '<mark data="36,*">Hannah</mark>'), 
    (782, 787, '<mark data="32,*">bully</mark>'),
    (29, 30, '<mark data="33,*">I</mark>'), 
    (67, 70, '<mark data="33,*">she</mark>'), 
    (144, 147, '<mark data="33,*">you</mark>'), 
    (191, 192, '<mark data="33,*">I</mark>'), 
    (202, 205, '<mark data="33,*">you</mark>'), 
    (235, 238, '<mark data="33,*">she</mark>'), 
    (248, 249, '<mark data="33,*">I</mark>'), 
    (278, 281, '<mark data="33,*">she</mark>'), 
    (316, 322, '<mark data="33,*">Hannah</mark>'), 
    (334, 336, '<mark data="33,*">we</mark>'), 
    (357, 363, '<mark data="33,*">Hannah</mark>'), 
    (402, 403, '<mark data="33,*">I</mark>'), 
    (415, 417, '<mark data="33,*">it</mark>'), 
    (443, 449, '<mark data="33,*">Hannah</mark>'), 
    (453, 459, '<mark data="33,*">Hannah</mark>'), 
    (491, 493, '<mark data="33,*">we</mark>'), 
    (530, 532, '<mark data="33,*">we</mark>'), 
    (558, 560, '<mark data="33,*">we</mark>'), 
    (580, 582, '<mark data="33,*">we</mark>'), 
    (718, 724, '<mark data="33,*">Hannah</mark>'), 
    (726, 728, '<mark data="37,*">it</mark>'), 
    (740, 743, '<mark data="33,*">you</mark>'), 
    (758, 760, '<mark data="37,*">it</mark>'), 
    (816, 819, '<mark data="33,*">she</mark>'), 
    (825, 827, '<mark data="37,*">it</mark>'), 
    (851, 854, '<mark data="33,*">her</mark>'), 
    (862, 868, '<mark data="33,*">Hannah</mark>'), 
    (872, 874, '<mark data="33,*">we</mark>'), 
    (890, 892, '<mark data="33,*">we</mark>'), 
    (904, 910, '<mark data="33,*">Hannah</mark>'), 
    (941, 943, '<mark data="33,*">we</mark>'), 
    (959, 965, '<mark data="33,*">Hannah</mark>'), 
    (997, 998, '<mark data="33,*">I</mark>'), 
    (1009, 1011, '<mark data="33,*">we</mark>'), 
    (1072, 1074, '<mark data="33,*">we</mark>'), 
    (1084, 1085, '<mark data="33,*">I</mark>'), 
    (73, 77, '<mark data="29,2">then</mark>'), 
    (351, 356, '<mark data="30,*">until</mark>'), 
    (450, 452, '<mark data="29,2">so</mark>'), 
    (475, 490, '<mark data="29,2">all of a sudden</mark>'), 
    (549, 557, '<mark data="29,2">But then</mark>'), 
    (616, 620, '<mark data="29,2">then</mark>'), 
    (761, 763, '<mark data="30,*">so</mark>'), 
    (774, 777, '<mark data="30,*">But</mark>'), 
    (813, 815, '<mark data="30,*">so</mark>'), 
    (869, 871, '<mark data="29,2">so</mark>'), 
    (932, 940, '<mark data="29,2">and then</mark>'), 
    (1004, 1008, '<mark data="29,2">then</mark>'), 
    (1062, 1066, '<mark data="30,*">then</mark>')
]

# Original text
original_text = '''One sunny morning my mum and I were cleaning out our grandfather’s shed, then my mum got a call from work and needed to go, she said to me “can you please stay and clean the shed?” "yes mum” I said “do you want a friend to come over?” she said “ok I’ll go call Hannah to see if she can come over” So my mum left and Hannah came over, we were cleaning until Hannah said “What’s in this little red box?” I said “Open it and find out.” “OK” said Hannah so Hannah opened the box all of a sudden we had gold and silver everywhere! And we ate a sandwich. But then we heard a big “BANG” we stopped and looked at each other then out of nowhere came a big bully and the bully said “Give me your gold and silver now!” “No” said Hannah “it’s ours and you’re not having it so go away!” But the bully didn’t like that at all. so she took it all and ran off “after her!” said Hannah so we ran as fast as we could, and Hannah opened the box again and then we had jet packs! Hannah said this box is magic! "Cool" I said then we caught the bully and got our gold and silver back then when we got home I opened the box and everything was back to normal.'''

# Function to insert marks in original text
def mark_text(original, positions):
    marked_text = original
    marked_indices = set()  # To keep track of already marked positions

    for start, end, mark in positions:
        # Check if this position has already been marked
        if not any(start < marked_start < end or start < marked_end < end for marked_start, marked_end in marked_indices):
            # Add the marked range to the set
            marked_indices.add((start, end))
            # Insert the mark in the original text
            marked_text = marked_text[:start] + mark + marked_text[start:end] + '</mark>' + marked_text[end:]

    return marked_text

# Generate the marked text
fixed_marked_text = mark_text(original_text, marked_positions)

# Print the result
print(fixed_marked_text)



