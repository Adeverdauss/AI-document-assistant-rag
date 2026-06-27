def split_text(text,
               chunk_size=1200,
               overlap=300):

    chunks=[]

    start=0

    length=len(text)

    while start < length:

        end=min(

            start+chunk_size,

            length

        )

        chunks.append(

            text[start:end]

        )

        start += chunk_size-overlap

    return chunks