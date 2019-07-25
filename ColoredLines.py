from LinesLive import main as live
from LinesRecorded import main as recorded
def main(l):
    if l:
        live()
        return
    recorded()
    return