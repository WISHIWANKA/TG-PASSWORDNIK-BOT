class TransPose:
    def __init__(self):
        pass

    def reverse(self, message: str):
        chars = list(message)
        start = 0
        end = len(chars) - 1
        while start < end:
            chars[start], chars[end] = chars[end], chars[start]
            start += 1
            end -= 1
        return "".join(chars)
