# import music21
# import simplejson as json
# # Function for basic info retrieval
# def getMusicInfo(midiFile):
#     stream = music21.converter.parse(midiFile)
#
#     def getTempo():
#         tempo = stream.flat.getElementsByClass('MetronomeMark')
#         if len(tempo) < 1:
#             return 0
#         else:
#             return tempo[-1].number
#
#     def getTimeSignature():
#         timeSignature = stream.flat.getElementsByClass('TimeSignature')
#         if len(timeSignature) < 1:
#             return 'unknown'
#         else:
#             return timeSignature[-1].ratioString
#
#     duration = stream.highestTime
#     key = stream.analyze('key')
#
#     return (getTempo(), getTimeSignature(), duration, key)
#
#
# def getTracks(midiFile):
#     stream = music21.converter.parse(midiFile)
#     iterators = []
#     noteList = []
#     offsetList = []
#     durationList = []
#     velocityList = []
#     for t in stream:
#         iterators.append(t.flat.getElementsByClass('Note'))
#     for t in iterators:
#         notes = []
#         offsets = []
#         durations = []
#         velocities = []
#         for n in t:
#             notes.append(int(n.pitch.midi))
#             offsets.append(float(n.offset))
#             durations.append(float(n.duration.quarterLength))
#             velocities.append(int(n.volume.velocity))
#         noteList.append(notes)
#         offsetList.append(offsets)
#         durationList.append(durations)
#         velocityList.append(velocities)
#     return (json.dumps({"noteList": noteList, "offsetList": offsetList, "durationList": durationList, "velocityList": velocityList}))
