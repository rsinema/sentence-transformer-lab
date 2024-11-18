# Sentence Transformer Lab

This repository contains experiments and projects related to sentence transformers.

## Introduction

This is project for my Natural Language Processing class. This uses sentence transformers to embed a bunch of technical eBooks that I have on my machine, and makes them searchable. I can input a question, which will get embedded, and then the _n_ nearest chunks from the data will be returned. Here is an example of a question and the chunks that are returned:

```bash
$ python ebook_search.py -q "How do I route traffic to my Docker container?"

Found 5 results:
Document: HowLinuxWorks3E.txt Distance: 0.3461887034065293
Content: e to reach outside hosts, the Docker network on the host configures NAT. Figure 17-1 shows a typical setup. It includes the physical layer with the interfaces, as well as the internet layer of the Docker subnet and the NAT linking this subnet to the rest of the host machine and its outside connections. Figure 17-1: Bridge network in Docker. The thick link represents the virtual interface pair bond. NOTE You might need to examine the subnet of your Docker interface network. There can sometimes be

Document: Learn_Docker_in_a_Month_of_Lunches.txt Distance: 0.37678825855254683
Content: chapter 2, this one doesn’t accept incoming traffic, so you don’t need to publish any ports. There’s one new flag in this command, which is --name. You know that you can work with containers using the ID that Docker generates, but you can also give them a friendly name. This container is called web-ping, and you can use that name to refer to the container instead of using the random ID. My blog is getting pinged by the app running in your container now. The app runs in an endless loop, and you c

Document: Learn_Docker_in_a_Month_of_Lunches.txt Distance: 0.3920647916813065
Content: ation image, publishing the host port and connecting to the nat network: docker container run -d -p 802:80 --network nat image-gallery You can browse to http: / / localhost:802 and you’ll see NASA’s Astronomy Picture of the Day. Figure 4.10 shows the image when I ran my containers. Figure 4.10 The Go web application, showing data fetched from the Java API Right now you’re running a distributed application across three containers. The Go web application calls the Java API to get details of the im

Document: Learn_Docker_in_a_Month_of_Lunches.txt Distance: 0.3971958340050007
Content: on port 80--you can see the traffic flow in figure 2.6. Figure 2.6 The physical and virtual networks for computers and containers In this example my computer is the machine running Docker, and it has the IP address 192.168.2.150 . That’s the IP address for my physical network, and it was assigned by the router when my computer connected. Docker is running a single container on that computer, and the container has the IP address 172.0.5.1 . That address is assigned by Docker for a virtual networ

Document: HowLinuxWorks3E.txt Distance: 0.3990007163285355
Content: on with a forwarding daemon called slirp4netns, container processes can reach the outside world. This is less capable; for example, containers cannot connect to one another. There’s a lot more to networking, including how to expose ports in the container’s network stack for external services to use, but the network topology is the most important thing to understand. Docker Operation At this point, we could continue with a discussion of the various other kinds of isolation and restrictions that D
```

## Installation

To install the necessary dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## Usage

A PGVector database is used to store the embeddings. Running `docker compose up -d` will start that up.

A CLI is used to create the tables and add documents to the database. Here is the CLI:

```bash
usage: ebook_search.py [-h] [-c] [-i] [-r] [-t] [-x] [-a ADD] [-d DIR] [-q QUERY] [--book] [-n NUM_RESULTS] [--data-size] [-v]

Document Database Management

options:
  -h, --help            show this help message and exit
  -c, --clear           Clear the database
  -i, --index           Create an index on the database
  -r, --reindex         Recreate the index on the database
  -t, --table           Create a table in the database
  -x, --drop-table      Drop the table in the database
  -a ADD, --add ADD     Add a document to the database
  -d DIR, --dir DIR     Add all files in a directory to the database
  -q QUERY, --query QUERY
                        Query the database with a question
  --book                Flag for query option that queries whole books instead of text chunks
  -n NUM_RESULTS, --num-results NUM_RESULTS
                        Number of results to return for a query
  --data-size           Print the size of the database
  -v, --verbose         Print verbose output
```

`.pdf` and `.epub` files are supported.

A API endpoint is also avaiable using `fastapi`. Set up the endpoint by running:

```bash
uvicorn api:app --reload
```

There's also a basic streamlit app that will interact with the API and display the results for the query. After setting the API up, run:

```bash
streamlit run app.py
```
