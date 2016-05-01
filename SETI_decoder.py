#!/usr/bin/env python3

from PIL import Image

# Guessed frame size
width = 359  # Initial set of 1's          a prime number!
height = 757 # Initial set of 000..001's  also a prime number!
frameCount = 7   # len(message) / (width*height) == 7
framesWithHeaders = [3, 4, 5, 6] # frames 3 and above seem to have information at the top of them

C = 299792458 # Speed of light

def chunker(list, size):
  for i in range(0, len(list), size):
    yield list[i: i+size]

def frame3headerDecoder(row1Positive, row1Negative, row2Positive, row2Negative):
  print('frame 3 row 1 positive length {}'.format(len(row1Positive)))
  print('frame 3 row 1 negative length {}'.format(len(row1Negative)))
  print('frame 3 row 2 positive length {}'.format(len(row2Positive)))
  print('frame 3 row 2 negative length {}'.format(len(row2Negative)))

  # print([i for i in chunker(row1Positive, 13)])
  # print([i for i in chunker(row1Negative, 13)])
  # print([i for i in chunker(row2Positive, 13)])
  # print([i for i in chunker(row2Negative, 13)])

  messageFrequency = 452129190
  messagePeriod = 1/messageFrequency
  messageWavelength = C/messageFrequency

  print('Received Message Frequency: ' + str(messageFrequency))
  print('Received Message Period: ' + str(messagePeriod))
  print('Received Message Wavelength: ' + str(messageWavelength))
  print()

  print('Xor')

  xorPositive = ['1' if int(a) ^ int(b) else '0' for a,b in zip(row1Positive, row2Positive)]
  print(int(''.join(xorPositive), 2))

  xorNegative = ['1' if int(a) ^ int(b) else '0' for a,b in zip(row1Positive[::-1], row2Positive[::-1])]
  print(int(''.join(xorNegative), 2))

  row1PositiveInt = int(row1Positive, 2)
  row1NegativeInt = int(row1Negative, 2)
  row2PositiveInt = int(row2Positive, 2)
  row2NegativeInt = int(row2Negative, 2)

  print()
  print('Interpreted as Int')
  print(row1PositiveInt)
  print(row2PositiveInt)
  print(row1NegativeInt)
  print(row2NegativeInt)

  print()
  print('Interpreted as fraction')
  print(row1PositiveInt / row2PositiveInt)
  print(row2PositiveInt / row1PositiveInt)
  print(row1NegativeInt / row2NegativeInt)
  print(row2NegativeInt / row1NegativeInt)

  print()
  print('Interpreted as fraction (read backwards)')
  print(int(row1Positive[::-1]) / int(row2Positive[::-1]))
  print(int(row2Positive[::-1]) / int(row1Positive[::-1]))
  print(int(row1Negative[::-1]) / int(row2Negative[::-1]))
  print(int(row2Negative[::-1]) / int(row1Negative[::-1]))


  """
            Assuming This V is the value given
  OurFrequency = (Oscilations / TheirSITime)
  TheirSITime = oscilations / OurFrequency
  """
  print()
  print('Guessing alient SI time assumning frequency')
  print(row1PositiveInt / messageFrequency)
  print(row1NegativeInt / messageFrequency)
  print(row2PositiveInt / messageFrequency)
  print(row2NegativeInt / messageFrequency)

  print()
  print('Guessing alient SI time assumning frequency (Read Backwards)')
  print(int(row1Positive[::-1], 2) / messageFrequency)
  print(int(row1Negative[::-1], 2) / messageFrequency)
  print(int(row2Positive[::-1], 2) / messageFrequency)
  print(int(row2Negative[::-1], 2) / messageFrequency)



def frame4headerDecoder(row1Positive, row1Negative, row2Positive, row2Negative):
  # print('frame 4 row 1 positive length {}'.format(len(row1Positive.strip('0'))))
  # print('frame 4 row 1 negative length {}'.format(len(row1Negative.strip('1'))))
  # print('frame 4 row 2 positive length {}'.format(len(row2Positive.strip('0'))))
  # print('frame 4 row 2 negative length {}'.format(len(row2Negative.strip('1'))))
  pass


def frame5headerDecoder(row1Positive, row1Negative, row2Positive, row2Negative):
  # print('frame 5 row 1 positive length {}'.format(len(row1Positive.strip('0'))))
  # print('frame 5 row 1 negative length {}'.format(len(row1Negative.strip('1'))))
  # print('frame 5 row 2 positive length {}'.format(len(row2Positive.strip('0'))))
  # print('frame 5 row 2 negative length {}'.format(len(row2Negative.strip('1'))))
  pass


def frame6headerDecoder(row1Positive, row1Negative, row2Positive, row2Negative):
  # print('frame 6 row 1 positive length {}'.format(len(row1Positive.strip('0'))))
  # print('frame 6 row 1 negative length {}'.format(len(row1Negative.strip('1'))))
  # print('frame 6 row 2 positive length {}'.format(len(row2Positive.strip('0'))))
  # print('frame 6 row 2 negative length {}'.format(len(row2Negative.strip('1'))))
  pass


with open('./SETI_message.txt', 'r') as file:

  message = file.read()
    
  for frame in range(frameCount):
    positiveHeader = ['', '']
    negativeHeader = ['', '']

    negativeImage = Image.new('1', (width, height))
    negativeCanvas = negativeImage.load()

    posativeImage = Image.new('1', (width, height))
    posativeCanvas = posativeImage.load()

    frameContainsHeader = frame in framesWithHeaders

    if frameContainsHeader:
      negativeHeaderImage = Image.new('1', (width, 2))
      negativeHeaderCanvas = negativeHeaderImage.load()

      positiveHeaderImage = Image.new('1', (width, 2))
      positiveHeaderCanvas = positiveHeaderImage.load()

    for x in range(width):
      for y in range(height):
        value = message[x + width * (y + frame * height)]

        posativeCanvas[x, y] = 1 if value == '1' else 0
        negativeCanvas[x, y] = 1 if value == '0' else 0

        if frameContainsHeader and y < 2:
          negativeHeaderCanvas[x, y] = 1 if value == '1' else 0
          positiveHeaderCanvas[x, y] = 1 if value == '0' else 0

          positiveHeader[y] += value
          negativeHeader[y] += '1' if value == '0' else '0'

    negativeImage.save('./SETI_message_frame_{}_negative.png'.format(frame))
    posativeImage.save('./SETI_message_frame_{}_positive.png'.format(frame))

    if frameContainsHeader:
      negativeHeaderImage.save('./SETI_message_frame_{}_header_negative.png'.format(frame))
      positiveHeaderImage.save('./SETI_message_frame_{}_header_positive.png'.format(frame))

# Frame 0 appears to be a calibration frame
# Frame 1 appears to be incremeting binary when read from left-to-right
# Frame 2 appears to be increasing prime numbers in binary
# Frame 3 appears to be a waveform, presumably of frequency used to transmit the message (452129190 Hz). 
