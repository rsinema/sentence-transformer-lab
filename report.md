# Sentence Transformer Report

## Table of Contents

1. [Introduction](#introduction)
2. [Methods](#methods)
3. [Output examples](#output-examples)
   - [all-MiniLM-L6-v2](#all-minilm-l6-v2)
     - [Chunk Length: 1024, Overlap: 128](#chunk-length-1024-overlap-128)
     - [Chunk Length: 512, Overlap: 128](#chunk-length-512-overlap-128)
   - [all-mpnet-base-v2](#all-mpnet-base-v2)
     - [Chunk Length: 1024, Overlap: 128](#chunk-length-1024-overlap-128)
     - [Chunk Length: 512, Overlap: 128](#chunk-length-512-overlap-128)
4. [Code](#code)
   - [Embedding code](#embedding-code)
   - [Database code](#vector-db-code)

## Introduction

For this project, I created a vector database that made the information in the ebooks on my machine queriable. My dad likes to read technical eBooks and he always shares them with me, but I never really have the time to read all of them, especially while I am still in school. I thought it would be a interesting and fun project to embed all these books into a database and try querying them with natural language questions. This project would be a good starting spot for a RAG application, that would take the information from the books as context to a question and generate a response to it based on the information in the books.

## Methods

I tried using 2 different sentence transformers to see if that would make the information retrieved more relevant to the given question. I used `all-MiniLM-L6-v2` and `all-mpnet-base-v2` to embed the documents. The books were stored in a `.epub` or `.pdf` format, so I used some python libraries to transform them into plaintext data. This data was then chunked into pieces that could be embedded, with a overlap into the next chunk. The embeddings were then stored in the database along with an offset to the beginning of that chunk. To query the data, a question is given in natural language which is then embedded with the same transformer that put the data in the database. The _n_ most similar chunks are found on cosine similarity, and those are returned to answer the question. I also made an option that would take the average embedding for each book, and compare the question's embedding to the book embeddings to recommend books that could answer the given question.

Both models performed well and were able to get information that was relevant to the question, as long as the question resided in the same domain as the information. Questions about topics such as Docker, Linux, Machine Learning, or Cloud Development worked well, because the information stored in the database is in those domains and was relevant to those questions. Questions from outside of the domain didn't work well, because there wasn't any relevant information about the question in the database.

Comparing the results from the two models, it seems the the `mpnet` model was slightly better at retrieving more relevant information from the books. When looking at the "What is cloud native development?" question, the data returned from both models was similar and they both seemed to perform well. The `mpnet` model is a little larger than the `MiniLM` model, so I assumed that `mpnet` would outperform `MiniLM`. If there were a couple hundred more books to add into the data or if more complex questions were asked, I think that `mpnet` would be able to retrieve more relevant information.

The only problem with that would be that the `mpnet` model took about 4-5 times as long to embed documents into the database as `MiniLM`. `MiniLM` was able to process an entire ebook (~300 pages) in about 5-15 seconds, while `mpnet` took about 45-55 seconds usually. I have around 85 ebooks on my machine currently, so `MiniLM` was able to process the entire library in 15-20 minutes, while `mpnet` took around a hour to complete all the books. For this toy example using just local data, it was no problem, but scaling this up to larger dataset would make a much more noticable and costly difference. With barely any drop in performance for using the smaller `MiniLM` model, using `MiniLM` would seem to be the better model to use if speed and complexity were an issue.

I tried different chunk lengths as well, 512 and 1024 chars, each with a 128 char overlap. The difference wasn't significant between the chunk lengths, 1024 seemed to capute the information better than 512. To get more context with the return, I used the offset and returned the found chunk, and the previous and next chunks in the same book. This made the information have more context and easier to read. I think that increasing the chunk size even more could have possibly increased the relevant information returned, but also could have diluted information for more specific or complex questions.

## Output examples

### all-MiniLM-L6-v2

#### Chunk Length: 1024, Overlap: 128

```bash
$ python ebook_search.py -q "What is TLS used for in cryptography?" -e
Found 5 results:
Document: securityandmicroservicearchitectureonaws.txt Distance: 0.4037579894065815
Content: ccess for subordinate CAs in the chain. Microservices can use the subordinate CAs for most of their known communication patterns while services such as service discovery, logging, and other centrally managed services can make use of the root CA. This flexibility is beneficial if you must identify a subject by a specific name or if you cannot rotate certificates easily. Encryption Using TLS The second important role that TLS plays in any given system is to provide end-to-end encryption of data that is in transit. Contrary to popular belief, TLS in itself is not an encryption algorithm. TLS instead defines certain steps that both the client and the server need to take in order to mutually decide which cipher works best for communication between them. In fact, one of the first steps of any TLS connection is a negotiation process where the client and the server mutually agree on which cipher works best for both of them. This information exchange happens during the phase of communication known as TLS Handshake. TLS Handshake is also used to exchange encryption keys for end-to-end encryption. This makes TLS Handshake one of the most crucial, yet often overlooked, aspects of communication between any two processes. TLS Handshake As mentioned, encryption using TLS is done using a symmetric key algorithm. This means that both the server and the client use the same encryption key as well as an encryption algorithm that they agree upon to encrypt the communication channel with. Various AWS services support a vast variety of ciphers, and the strongest cipher is chosen based on a waterfall process of selection. A waterfall process is where the server creates a list of ciphers that it supports in the descending order of strength. The client agrees to use the strongest cipher that it can support within that list. Thus, the server and the client mutually decide on what they believe is the best common algorithm that is supported by both parties. Note AWS regularly updates the list of supported ciphers in its documentation; using

Document: CryptoDictionary.txt Distance: 0.43141359090804654
Content: lock puzzle paper proposed an actual challenge, and they made the following prediction: We estimate that the puzzle will require 35 years of continuous computation to solve, with the computer being replaced every year by the next fastest model available. In 2019, this challenge was shown to be quite a bit easier to solve, using either a desktop CPU or FPGA (in which case it took only two months of computation). Although it was an interesting thought experiment of negligible practical interest, at least regarding the time-travel aspects, the initial paper suggested periods of months or years of computation. Timing attack An attack that takes advantage of timing differences to discover a secret and more generally compromise a cryptosystem’s security. Sometimes, the running time of the algorithm depends on the value of secret inputs, which might trigger things, such as if–then patterns or some other ­variable-time operation. For example, some processors’ arithmetic units will execute a multiplication instruction in fewer cycles if one of the inputs is zero. The textbook example of a timing attack targets square-and-multiply exponentiation (or double-and-add multiplication) where the private exponent (or scalar) is scanned bit per bit. Attackers can also exploit timing leaks to identify the outcome of a cryptographic operation (such as padding validation) or the type of error that occurs when no detailed error code is returned (as with mitigations against Manger’s attack). TLS (Transport Layer Security) A protocol to establish a secure channel over TCP (and over UDP with DTLS). TLS used PKI, X.509 certificates, and too many cipher suites until TLS 1.3. See SSL, Heartbleed. INDUSTRY CONCERNS In September 2016, during the development of TLS 1.3, a representative of a financial services organization sent an email to the IETF working group in charge of TLS with the subject line Industry Concerns about TLS 1.3. The message requested that TLS 1.3 consider integrating features allowing supervised employee communications (as

Document: securityandmicroservicearchitectureonaws.txt Distance: 0.43702043780623334
Content: on ways in which malicious actors can gain unauthorized access to the data that is being communicated or is in transit. Figure 7-2 shows a standard communication between a service (Service A) and a credit card processor service (CCPS). Figure 7-2. “Phishing” and “man in the middle” are two of the most common ways in which malicious actors steal user data while in transit. Let’s assume Service A needs to send sensitive information to the CCPS. There are two ways in which malicious actors may try to steal this sensitive information: Phishing An imposter could pretend to be the CCPS. If Service A has no way of identifying the real CCPS, it may end up sending sensitive information to the imposter. Man in the middle Another service could start snooping and recording all the data that is being exchanged legitimately between Service A and CCPS and thus come across sensitive information. TLS reduces the risk of these potential threats by helping you implement authentication and encryption controls on the communication channels. In the following section, I will explain in detail how authentication and encryption work to reduce this risk: Authentication The purpose of authentication is to identify and validate the identity of a server in a communication channel. Under TLS, both parties, the client and the server, agree to entrust the authentication task to a trusted party called a trusted certificate authority (trusted CA). Through the use of digital certificates and public key encryption, a trusted CA can verify the identity of the server to a client that has trusted the CA. Server validation can help to prevent impersonation and phishing attacks. Encryption Encryption aims to ensure that any communication between the service provider and the service consumer cannot be accessed by a third party. This is done using end-to-end encryption that TLS provides after a secure line has been established. Through encryption, TLS can help prevent man-in-the-middle or communication channel hijacking attacks. Note We live today in a wo

Document: learningdapr.txt Distance: 0.45056039684290927
Content: romised, the adversary can gain access to all the secrets in the secret store. With integration with service identities (see “Identity”), Dapr is able to offer some automatic authentication and authorization mechanisms to constrain access to secrets. For example, it can enforce a policy that grants an application access only to a particular secret store or even specific secret keys. Then, even when an application is compromised, the attacker won’t be able to use the application to gain access to the secrets of other applications sharing the same secret store. That’s about all Dapr provides in terms of secret management. Next, we’ll shift gears and talk about how Dapr secures Dapr-to-Dapr communications through mutual TLS. Mutual TLS (mTLS) Transport Layer Security (TLS), which replaces the deprecated Secure Sockets Layer (SSL) protocol, is a cryptographic protocol used for secure communication between clients and servers. By default, TLS proves the server’s identity to the client using a server X.509 certificate. Optionally, it can also prove the client’s identity to the server using a client X.509 certificate. This is called mutual TLS. Mutual TLS (mTLS) is often used in distributed systems because in such systems it’s hard to identify a server or a client. Instead, components call each other in a mesh, so any component can be both a server and a client. Mutual TLS ensures all service calls among components are authenticated on both sides by cross-checking the certificates. Before introducing how mTLS works, we need to provide a brief explanation of certificates and related concepts. If you are familiar with these concepts already, you can skip the following subsections. X.509 certificates An X.509 certificate is a digital certificate using the international X.509 public key infrastructure (PKI) standard. A certificate is issued by a trusted certificate authority (CA) and contains information about the represented entity such as the verified entity name and validity period of the certificate. A certificate also

Document: NetworkProgrammingWithGo.txt Distance: 0.46575781907094504
Content: pplications should be no different. We should strive to authenticate our communication and use encryption where appropriate, particularly when that information has the potential to leak over insecure networks. Up to this point, we’ve used TLS only as an afterthought in our code. This is partly because Go’s net/http library makes its use relatively effortless, but it’s also because we haven’t adequately explored the TLS protocol and the infrastructure that makes it possible. To write secure software, you should carefully plan for security before development starts and then use good security practices as you write code. TLS is a terrific way to improve the security posture of your software by protecting data in transit. This chapter will introduce you to the basics of TLS from a programmer’s perspective. You’ll learn about the client-server handshake process and the inherent trust that makes that process work. Then we’ll discuss how things can (and do) go wrong even when you use TLS. Finally, we’ll look at practical examples of how to incorporate TLS into your applications, including mutual client-server authentication. A Closer Look at Transport Layer Security The TLS protocol supplies secure communication between a client and a server. It allows the client to authenticate the server and optionally permits the server to authenticate clients. The client uses TLS to encrypt its communication with the server, preventing third-party interception and manipulation. TLS uses a handshake process to establish certain criteria for the stateful TLS session. If the client initiated a TLS 1.3 handshake with the server, it would go something like this: Client Hello google.com. I’d like to communicate with you using TLS version 1.3. Here is a list of ciphers I’d like to use to encrypt our messages, in order of my preference. I generated a public- and private-key pair specifically for this conversation. Here’s my public key. Server Greetings, client. TLS version 1.3 suits me fine. Based on your cipher list, I’ve decided we’ll use
```

```bash
$ python ebook_search.py -q "What is cloud native development?" -e
Found 5 results:
Document: cloudnativedevelopmentwithgooglecloud.txt Distance: 0.1826763153076172
Content: t seeks to adopt a cloud native development style. Either way, your skills will be highly sought after and valuable. I recall a conference speaker’s words from the late 2000s, as smartphones began to dominate the market. They described mobile phone manufacturers and network operators as engaged in a war, with mobile app developers serving as the ammunition. Today, as organizations strive to exploit the cloud’s full potential, cloud native developers have become the new ammunition. This book consolidates my learnings over the years to help you experience the same joy—a term I use with utmost sincerity—that I have derived as a cloud native developer. It aims to offer you an accessible and low-cost route to experiencing the productivity of cloud native development as an individual, by crafting a developer experience (DX) that truly works for you. Additionally, it offers enough insight into enterprise concerns to successfully introduce cloud native development into a scaled environment. Achieving the same level of productivity at work as in your personal projects can help you experience this joy at the workplace as well. Summary Cloud native represents an architectural approach and development methodology that fully exploits the potential of the cloud. It’s characterized by specific techniques, tools, and technologies designed to enhance the strengths and mitigate the weaknesses inherent in cloud computing. Importantly, the scope of cloud native isn’t confined to Google Cloud or even the public cloud. It encompasses a broad spectrum of methodologies applicable wherever cloudlike abstractions are present. To thrive in the cloud native ecosystem, developers need to harness the potential of four distinct yet interdependent facilities: a laboratory for innovative exploration, a factory for streamlined production automation, a citadel for robust defense of live applications, and an observatory for comprehensive system oversight. The remainder of this book will guide you through these cloud native methodologies, demonstrat

Document: cloudnativedevelopmentwithgooglecloud.txt Distance: 0.2241488427938355
Content: a different approach. When navigated adeptly, it can unlock a world of opportunities far surpassing those offered by traditional infrastructure. Embrace the differences, and the cloud’s full potential is vast. Embracing the Cloud as a Distributed System The essential truth of the cloud is that it functions as a distributed system. This key characteristic renders many assumptions inherent in traditional development obsolete. These misconceptions, dubbed the fallacies of distributed computing, were first identified by L Peter Deutsch and colleagues at Sun Microsystems: The network is reliable. Latency is zero. Bandwidth is infinite. The network is secure. Topology doesn’t change. There is one administrator. Transport cost is zero. The network is homogeneous. Each of these points represents a hurdle that must be surmounted when attempting to construct a cloud from scratch. Thankfully, cloud providers have devoted substantial engineering resources over the past two decades to build higher-level abstractions through APIs, effectively addressing these issues. This is precisely why digital natives have an edge—they are attuned to cloud native development, a methodology that leverages this groundwork. Cloud native development acknowledges the distinct characteristics of the cloud and capitalizes on the high-level abstractions provided by cloud provider APIs. It’s a development style in tune with the realities of the cloud, embracing its idiosyncrasies and leveraging them to their full potential. Distinguishing Cloud Hosted from Cloud Native Understanding the difference between cloud hosted and cloud native applications is fundamental. To put it simply, the former is about where, and the latter is about how. Applications can be cloud hosted, running on infrastructure provided by a public cloud provider, but architectured traditionally, as if they were operating in an on-premises data center. Conversely, applications can be designed in a cloud native manner and still be hosted in an on-premises data center, as shown in Fig

Document: cloudnativedevelopmentwithgooglecloud.txt Distance: 0.22622959457459346
Content: oud providers have devoted substantial engineering resources over the past two decades to build higher-level abstractions through APIs, effectively addressing these issues. This is precisely why digital natives have an edge—they are attuned to cloud native development, a methodology that leverages this groundwork. Cloud native development acknowledges the distinct characteristics of the cloud and capitalizes on the high-level abstractions provided by cloud provider APIs. It’s a development style in tune with the realities of the cloud, embracing its idiosyncrasies and leveraging them to their full potential. Distinguishing Cloud Hosted from Cloud Native Understanding the difference between cloud hosted and cloud native applications is fundamental. To put it simply, the former is about where, and the latter is about how. Applications can be cloud hosted, running on infrastructure provided by a public cloud provider, but architectured traditionally, as if they were operating in an on-premises data center. Conversely, applications can be designed in a cloud native manner and still be hosted in an on-premises data center, as shown in Figure 1-4. Figure 1-4. Cloud hosted is where, cloud native is how When I refer to cloud native, I am discussing the development style, application architecture, and abstraction provided by the cloud APIs, rather than the hosting location. This book primarily explores the construction of cloud native applications using Google Cloud, which embraces both cloud hosted and cloud native principles, the bottom right in Figure 1-4. However, keep in mind that much of the information shared here is also applicable to on-premises private and hybrid clouds, particularly those built around containers and Kubernetes, such as Red Hat OpenShift, VMWare Tanzu and Google Anthos, bottom left in Figure 1-4. Unraveling the Concept of Cloud Native The term “cloud native” used to make me cringe, as I felt its significance had been diluted by software vendors leveraging it merely as a stamp of approval to sign

Document: cloudnativedevelopmentwithgooglecloud.txt Distance: 0.23114696833929294
Content: handed a Kubernetes cluster and expected to manage it, problems are bound to arise. A common misconception is that cloud native begins and ends with containers or Kubernetes, but this is far from the truth. There are also issues related to cost and security. Both these aspects undergo significant changes with the cloud, especially in a cloud native scenario. Developers need to work within appropriate boundaries to prevent costly mistakes or security breaches that could compromise an organization’s reputation. What’s more crucial in the CNCF definition is the second part—the techniques. These reflect a development style that capitalizes on the cloud’s strengths while recognizing its limitations. Cloud native is about acknowledging that hardware will fail, networks can be unreliable, and user demand will fluctuate. Moreover, modern applications need to continuously adapt to user requirements and should, therefore, be designed with this flexibility in mind. The concept of cloud native extends to considering the cloud’s limitations as much as utilizing its benefits. Embracing cloud native means a mental shift toward designing applications to make the most of the abstractions exposed by cloud providers’ APIs. This implies a transition from thinking in terms of hardware elements such as servers, disks, and networks to higher abstractions like units of compute, storage, and bandwidth. Importantly, cloud native is geared toward addressing key issues: Developing applications that are easy to modify Creating applications that are more efficient and reliable than the infrastructure they run on Establishing security measures that are based on a zero-trust model The ultimate goal of cloud native is to achieve short feedback cycles, zero downtime, and robust security. So, “cloud native” no longer makes me cringe; it encapsulates and communicates a style of development that overcomes the cloud’s limitations and unlocks its full potential. In essence, cloud native acts as a catalyst, making the initial promise of cloud computing

Document: cloudnativedevelopmentwithgooglecloud.txt Distance: 0.23247593641281128
Content:  declarative APIs exemplify this approach. These techniques enable loosely coupled systems that are resilient, manageable, and observable. Combined with robust automation, they allow engineers to make high-impact changes frequently and predictably with minimal toil. In my early advocacy for cloud native technology, I commonly characterized it as encompassing microservices, containers, automation, and orchestration. However, this was a misstep; while these are vital components of a cloud native solution, they are just the technological aspects referenced in the first part of CNCF’s definition. Mistaking cloud native as purely a technological shift is one of the key reasons why many cloud native initiatives fail. Introducing technologies like Kubernetes can be quite disruptive due to the steep learning curve and the added complexity they present to developers. If developers are merely handed a Kubernetes cluster and expected to manage it, problems are bound to arise. A common misconception is that cloud native begins and ends with containers or Kubernetes, but this is far from the truth. There are also issues related to cost and security. Both these aspects undergo significant changes with the cloud, especially in a cloud native scenario. Developers need to work within appropriate boundaries to prevent costly mistakes or security breaches that could compromise an organization’s reputation. What’s more crucial in the CNCF definition is the second part—the techniques. These reflect a development style that capitalizes on the cloud’s strengths while recognizing its limitations. Cloud native is about acknowledging that hardware will fail, networks can be unreliable, and user demand will fluctuate. Moreover, modern applications need to continuously adapt to user requirements and should, therefore, be designed with this flexibility in mind. The concept of cloud native extends to considering the cloud’s limitations as much as utilizing its benefits. Embracing cloud native means a mental shift toward designing applications
```

```bash
$ python ebook_search.py -q "What is cloud native development?" -b
Found 5 results:
Document: cloudnativedevelopmentwithgooglecloud.txt
Distance: 0.39102677307784917

Document: architectingiotsolutionsonazure.txt
Distance: 0.497594172344181

Document: architectingdataandmachinelearningplatforms.txt
Distance: 0.5197969609120754

Document: clouddatalake.txt
Distance: 0.5374795336475715

Document: genomicsintheazurecloud.txt
Distance: 0.5866395774593247
```

#### Chunk Length: 512, Overlap: 128

```bash
$ python ebook_search.py -q "What is cloud native development" -e
Found 5 results:
Document: cloudnativedevelopmentwithgooglecloud.txt Distance: 0.1411231587978351
Content: gy doesn’t change. There is one administrator. Transport cost is zero. The network is homogeneous. Each of these points represents a hurdle that must be surmounted when attempting to construct a cloud from scratch. Thankfully, cloud providers have devoted substantial engineering resources over the past two decades to build higher-level abstractions through APIs, effectively addressing these issues. This is precisely why digital natives have an edge—they are attuned to cloud native development, a methodology that leverages this groundwork. Cloud native development acknowledges the distinct characteristics of the cloud and capitalizes on the high-level abstractions provided by cloud provider APIs. It’s a development style in tune with the realities of the cloud, embracing its idiosyncrasies and leveraging them to their full potential. Distinguishing Cloud Hosted from Cloud Native Understanding the difference between cloud hosted and cloud native applications is fundamental. To put it simply, the former is about

Document: cloudnativedevelopmentwithgooglecloud.txt Distance: 0.1584471118912778
Content: erience the same joy—a term I use with utmost sincerity—that I have derived as a cloud native developer. It aims to offer you an accessible and low-cost route to experiencing the productivity of cloud native development as an individual, by crafting a developer experience (DX) that truly works for you. Additionally, it offers enough insight into enterprise concerns to successfully introduce cloud native development into a scaled environment. Achieving the same level of productivity at work as in your personal projects can help you experience this joy at the workplace as well. Summary Cloud native represents an architectural approach and development methodology that fully exploits the potential of the cloud. It’s characterized by specific techniques, tools, and technologies designed to enhance the strengths and mitigate the weaknesses inherent in cloud computing. Importantly, the scope of cloud native isn’t confined to Google Cloud or even the public cloud. It encompasses a broad spectrum of methodologies appl

Document: cloudnativedevelopmentwithgooglecloud.txt Distance: 0.16789098073025788
Content: ud is that it functions as a distributed system. This key characteristic renders many assumptions inherent in traditional development obsolete. These misconceptions, dubbed the fallacies of distributed computing, were first identified by L Peter Deutsch and colleagues at Sun Microsystems: The network is reliable. Latency is zero. Bandwidth is infinite. The network is secure. Topology doesn’t change. There is one administrator. Transport cost is zero. The network is homogeneous. Each of these points represents a hurdle that must be surmounted when attempting to construct a cloud from scratch. Thankfully, cloud providers have devoted substantial engineering resources over the past two decades to build higher-level abstractions through APIs, effectively addressing these issues. This is precisely why digital natives have an edge—they are attuned to cloud native development, a methodology that leverages this groundwork. Cloud native development acknowledges the distinct characteristics of the cloud and capitalizes

Document: cloudnativedevelopmentwithgooglecloud.txt Distance: 0.19275813145885778
Content:  and abstraction provided by the cloud APIs, rather than the hosting location. This book primarily explores the construction of cloud native applications using Google Cloud, which embraces both cloud hosted and cloud native principles, the bottom right in Figure 1-4. However, keep in mind that much of the information shared here is also applicable to on-premises private and hybrid clouds, particularly those built around containers and Kubernetes, such as Red Hat OpenShift, VMWare Tanzu and Google Anthos, bottom left in Figure 1-4. Unraveling the Concept of Cloud Native The term “cloud native” used to make me cringe, as I felt its significance had been diluted by software vendors leveraging it merely as a stamp of approval to signify their applications are cloud compatible and modern. It reminded me of other buzzwords such as “agile” or “DevOps,"” which have been reshaped over time by companies with something to sell. Nevertheless, the Cloud Native Computing Foundation (CNCF), a Linux Foundation project establ

Document: cloudnativedevelopmentwithgooglecloud.txt Distance: 0.2137006607769344
Content: 2000s, as smartphones began to dominate the market. They described mobile phone manufacturers and network operators as engaged in a war, with mobile app developers serving as the ammunition. Today, as organizations strive to exploit the cloud’s full potential, cloud native developers have become the new ammunition. This book consolidates my learnings over the years to help you experience the same joy—a term I use with utmost sincerity—that I have derived as a cloud native developer. It aims to offer you an accessible and low-cost route to experiencing the productivity of cloud native development as an individual, by crafting a developer experience (DX) that truly works for you. Additionally, it offers enough insight into enterprise concerns to successfully introduce cloud native development into a scaled environment. Achieving the same level of productivity at work as in your personal projects can help you experience this joy at the workplace as well. Summary Cloud native represents an architectural approach
```

```bash
$ python ebook_search.py -q "What is cloud native development" -b
Found 5 results:
Document: cloudnativedevelopmentwithgooglecloud.txt
Distance: 0.3780395321993183

Document: architectingiotsolutionsonazure.txt
Distance: 0.5120754040051012

Document: architectingdataandmachinelearningplatforms.txt
Distance: 0.5532270381762798

Document: genomicsintheazurecloud.txt
Distance: 0.5748786372311467

Document: clouddatalake.txt
Distance: 0.576494306865573
```

### all-mpnet-base-v2

#### Chunk Length: 1024, Overlap: 128

```bash
python ebook_search.py -q "What is cloud native development" -e
Found 5 results:
Document: cloudnativedevelopmentwithgooglecloud.txt Distance: 0.20994965970814994
Content: handed a Kubernetes cluster and expected to manage it, problems are bound to arise. A common misconception is that cloud native begins and ends with containers or Kubernetes, but this is far from the truth. There are also issues related to cost and security. Both these aspects undergo significant changes with the cloud, especially in a cloud native scenario. Developers need to work within appropriate boundaries to prevent costly mistakes or security breaches that could compromise an organization’s reputation. What’s more crucial in the CNCF definition is the second part—the techniques. These reflect a development style that capitalizes on the cloud’s strengths while recognizing its limitations. Cloud native is about acknowledging that hardware will fail, networks can be unreliable, and user demand will fluctuate. Moreover, modern applications need to continuously adapt to user requirements and should, therefore, be designed with this flexibility in mind. The concept of cloud native extends to considering the cloud’s limitations as much as utilizing its benefits. Embracing cloud native means a mental shift toward designing applications to make the most of the abstractions exposed by cloud providers’ APIs. This implies a transition from thinking in terms of hardware elements such as servers, disks, and networks to higher abstractions like units of compute, storage, and bandwidth. Importantly, cloud native is geared toward addressing key issues: Developing applications that are easy to modify Creating applications that are more efficient and reliable than the infrastructure they run on Establishing security measures that are based on a zero-trust model The ultimate goal of cloud native is to achieve short feedback cycles, zero downtime, and robust security. So, “cloud native” no longer makes me cringe; it encapsulates and communicates a style of development that overcomes the cloud’s limitations and unlocks its full potential. In essence, cloud native acts as a catalyst, making the initial promise of cloud computing

Document: cloudnativedevelopmentwithgooglecloud.txt Distance: 0.2177856071782972
Content: vided by a public cloud provider, but architectured traditionally, as if they were operating in an on-premises data center. Conversely, applications can be designed in a cloud native manner and still be hosted in an on-premises data center, as shown in Figure 1-4. Figure 1-4. Cloud hosted is where, cloud native is how When I refer to cloud native, I am discussing the development style, application architecture, and abstraction provided by the cloud APIs, rather than the hosting location. This book primarily explores the construction of cloud native applications using Google Cloud, which embraces both cloud hosted and cloud native principles, the bottom right in Figure 1-4. However, keep in mind that much of the information shared here is also applicable to on-premises private and hybrid clouds, particularly those built around containers and Kubernetes, such as Red Hat OpenShift, VMWare Tanzu and Google Anthos, bottom left in Figure 1-4. Unraveling the Concept of Cloud Native The term “cloud native” used to make me cringe, as I felt its significance had been diluted by software vendors leveraging it merely as a stamp of approval to signify their applications are cloud compatible and modern. It reminded me of other buzzwords such as “agile” or “DevOps,"” which have been reshaped over time by companies with something to sell. Nevertheless, the Cloud Native Computing Foundation (CNCF), a Linux Foundation project established to bolster the tech industry’s efforts toward advancing cloud native technologies, provides a concise definition: Cloud native technologies empower organizations to build and run scalable applications in modern, dynamic environments such as public, private, and hybrid clouds. Containers, service meshes, microservices, immutable infrastructure, and declarative APIs exemplify this approach. These techniques enable loosely coupled systems that are resilient, manageable, and observable. Combined with robust automation, they allow engineers to make high-impact changes frequently and predictably with mi

Document: cloudnativedevelopmentwithgooglecloud.txt Distance: 0.22742444276807494
Content: a different approach. When navigated adeptly, it can unlock a world of opportunities far surpassing those offered by traditional infrastructure. Embrace the differences, and the cloud’s full potential is vast. Embracing the Cloud as a Distributed System The essential truth of the cloud is that it functions as a distributed system. This key characteristic renders many assumptions inherent in traditional development obsolete. These misconceptions, dubbed the fallacies of distributed computing, were first identified by L Peter Deutsch and colleagues at Sun Microsystems: The network is reliable. Latency is zero. Bandwidth is infinite. The network is secure. Topology doesn’t change. There is one administrator. Transport cost is zero. The network is homogeneous. Each of these points represents a hurdle that must be surmounted when attempting to construct a cloud from scratch. Thankfully, cloud providers have devoted substantial engineering resources over the past two decades to build higher-level abstractions through APIs, effectively addressing these issues. This is precisely why digital natives have an edge—they are attuned to cloud native development, a methodology that leverages this groundwork. Cloud native development acknowledges the distinct characteristics of the cloud and capitalizes on the high-level abstractions provided by cloud provider APIs. It’s a development style in tune with the realities of the cloud, embracing its idiosyncrasies and leveraging them to their full potential. Distinguishing Cloud Hosted from Cloud Native Understanding the difference between cloud hosted and cloud native applications is fundamental. To put it simply, the former is about where, and the latter is about how. Applications can be cloud hosted, running on infrastructure provided by a public cloud provider, but architectured traditionally, as if they were operating in an on-premises data center. Conversely, applications can be designed in a cloud native manner and still be hosted in an on-premises data center, as shown in Fig

Document: cloudnativedevelopmentwithgooglecloud.txt Distance: 0.22975871208205723
Content:  declarative APIs exemplify this approach. These techniques enable loosely coupled systems that are resilient, manageable, and observable. Combined with robust automation, they allow engineers to make high-impact changes frequently and predictably with minimal toil. In my early advocacy for cloud native technology, I commonly characterized it as encompassing microservices, containers, automation, and orchestration. However, this was a misstep; while these are vital components of a cloud native solution, they are just the technological aspects referenced in the first part of CNCF’s definition. Mistaking cloud native as purely a technological shift is one of the key reasons why many cloud native initiatives fail. Introducing technologies like Kubernetes can be quite disruptive due to the steep learning curve and the added complexity they present to developers. If developers are merely handed a Kubernetes cluster and expected to manage it, problems are bound to arise. A common misconception is that cloud native begins and ends with containers or Kubernetes, but this is far from the truth. There are also issues related to cost and security. Both these aspects undergo significant changes with the cloud, especially in a cloud native scenario. Developers need to work within appropriate boundaries to prevent costly mistakes or security breaches that could compromise an organization’s reputation. What’s more crucial in the CNCF definition is the second part—the techniques. These reflect a development style that capitalizes on the cloud’s strengths while recognizing its limitations. Cloud native is about acknowledging that hardware will fail, networks can be unreliable, and user demand will fluctuate. Moreover, modern applications need to continuously adapt to user requirements and should, therefore, be designed with this flexibility in mind. The concept of cloud native extends to considering the cloud’s limitations as much as utilizing its benefits. Embracing cloud native means a mental shift toward designing applications

Document: cloudnativedevelopmentwithgooglecloud.txt Distance: 0.24448826974769655
Content: s designed to allow a clear understanding of its state from its external outputs. This observability can be facilitated through comprehensive logging, detailed metrics, effective visualization tools, and proactive alert systems. Declarative management In a cloud native environment, the underlying hardware is managed by someone else, with layers of abstraction built on top to simplify operations. Cloud native systems prefer a declarative approach to management, prioritizing the desired outcome (what) over the specific steps to achieve it (how). This management style allows developers to focus more on addressing business challenges. Zero-trust security Given that everything on the public cloud is shared, a default stance of zero trust is essential. Cloud native systems encrypt data both at rest and in transit and rigorously verify every interaction between components. As I explore these principles in later chapters, I will examine how various tools, technologies, and techniques can facilitate these concepts. Building a Cloud Native Platform Cloud providers offer a broad range of tools and technologies. For cloud native architecture to flourish, it is crucial to synergize these tools and apply them using cloud native techniques. This approach will lay the foundation for a platform conducive to efficient cloud native application development. Laboratory, Factory, Citadel, and Observatory When conceptualizing a cloud native platform, envision the construction of four key “facilities” on top of the cloud: the laboratory, factory, citadel, and observatory, as shown in Figure 1-6. Each one serves a specific purpose to promote productivity, efficiency, and security: Laboratory The laboratory maximizes developer productivity by providing a friction-free environment equipped with the necessary tools and resources for application innovation and development. It should foster a safe environment conducive to experimentation and rapid feedback. Factory The factory prioritizes efficiency. It processes the application—originally cr
```

```bash
python ebook_search.py -q "What is cloud native development" -b
Found 5 results:
Document: cloudnativedevelopmentwithgooglecloud.txt
Distance: 0.39987954487994537

Document: buildingserverlessapplicationsonknative.txt
Distance: 0.5304869613687462

Document: architectingiotsolutionsonazure.txt
Distance: 0.5423916151626024

Document: learningserverless.txt
Distance: 0.5522911436738256

Document: learningdapr.txt
Distance: 0.5543513807019658
```

```bash
python ebook_search.py -q "How is Deep Learning used?"
Found 5 results:
Document: insidedeeplearning.txt Distance: 0.31595311665814296
Content: ation problems. Examples include the following: Sentiment detection—Is this sequence of words (e.g., a sentence, tweet, or paragraph) indicating a positive, negative, or neutral impression? For example, I might run sentence detection on Twitter to find out if people like this book. Vehicle maintenance—Your car may store daily or weekly information about how many miles have been driven, miles per gallon while driving, engine temperature, and more. This could be used to predict whether a car will need repairs in the next 3, 6, or 12 months, often called predictive maintenance. Weather prediction—Every day, you can record the high, mean, and low temperature, humidity, wind speed, and so on. Then you can predict tons of things like the temperature the next day, how many people will go to the mall (companies would love to know that), and if traffic will be normal, bad, or good. RNNs are often challenging for people to grasp when diving into deep learning, and many materials treat them as magic black boxes that tak

Document: computerarchitecture.txt Distance: 0.3208360694343908
Content: our lives. These sorts of devices enable smart cities, smart agriculture, smart transport, and the Internet of Things. At the same time, these devices collect vast quantities of data—what we now call big data—and processing that data requires a second, new type of computer: extremely large supercomputers or compute clusters located in purpose-built sites the size of factories. Inside these buildings there are no people, only rows of blinking server lights. You may have heard of deep learning, a rebranding of the 60-year-old neural network algorithm. It could be argued that deep learning isn’t a branch of machine learning or AI theory at all, but rather a branch of computer architecture. After all, it’s new architectures, based on massive hardware parallelization through clusters of GPUs and custom silicon, that have brought the old algorithm up to speed, enabling it to run at scales many orders of magnitude larger than before. Thanks to these advances in computer architecture, we can finally use neural networ

Document: architectingdataandmachinelearningplatforms.txt Distance: 0.32785685922421703
Content: see Figure 10-1) that solves AI problems using data instead of custom logic. This makes it particularly useful when you can’t articulate the logic or if the logic will be too difficult to code up as a computer program. Instead of capturing all the differences between nails and screws, for example, an ML system is shown hundreds of nails and told they are nails, and hundreds of screws and told they are screws. The ML model then figures out how to tell them apart by tuning an internal, very general mathematical function. ML is many decades old, but until about 2014 it worked only on structured data of the sort that you can store in a database. Deep learning is a subfield of ML that shot into prominence in the late 2010s. It uses highly complex functions (which add “depth” to a pictorial representation of the function, hence its name). Deep learning has been successfully used to understand unstructured data like speech, images, video, and natural language. Deep learning is why you have been seeing smart speakers

Document: insidedeeplearning.txt Distance: 0.3290640515646892
Content: n Understanding automatic differentiation as the basis of learning Using the Dataset interface to prepare data Deep learning, also called neural networks or artificial neural networks, has led to dramatic advances in machine learning quality, accuracy, and usability. Technology that was considered impossible 10 years ago is now widely deployed or considered technically possible. Digital assistants like Cortana, Google, Alexa, and Siri are ubiquitous and can react to natural spoken language. Self-driving cars have been racking up millions of miles on the road as they are refined for eventual deployment. We can finally catalog and calculate just how much of the internet is made of cat photos. Deep learning has been instrumental to the success of all these use cases and many more. This book exposes you to some of the most common and useful techniques in deep learning today. A significant focus is how to use and code these networks and how and why they work at a deep level. With a deeper understanding, you’ll be

Document: deitel_pythonforprogrammers.txt Distance: 0.3302342098811728
Content: d take advantage of cameras and other sensors by using deep- learning computer-vision techniques to analyze images “on the fly” and automat- ically report those items. We introduce deep learning for computer vision in Chapter 15. 1.9 Intro to Data Science: Artificial Intelligence—at the Intersection of CS and Data Science When a baby first opens its eyes, does it “see” its parent’s faces? Does it understand any notion of what a face is—or even what a simple shape is? Babies must “learn” the world around them. That’s what artificial intelligence (AI) is doing today. It’s looking at massive amounts of data and learning from it. AI is being used to play games, implement a wide range of computer-vision applications, enable self-driving cars, enable robots to learn to perform new tasks, diagnose medical conditions, translate speech to other languages in near real time, create chatbots that can respond to arbitrary questions using massive data- bases of knowledge, and much more. Who’d have guessed just a few years
```

#### Chunk Length: 512, Overlap: 128

```bash
$ python ebook_search.py -q "What is gradient descent?" -e
Found 5 results:
Document: secretlifeofprograms.txt Distance: 0.24693664944926563
Content: e are weights in multiple layers, such as we saw in Figure 14-30. Figure 14-33: Gradient topology You might have noticed the mysterious disappearance of the output pulsing mechanism that we saw in Figure 14-27. The neural networks that we’ve seen so far are essentially combinatorial logic, not sequential logic, and are effectively DAGs. There is a sequential logic variation called a recurrent neural network. It’s not a DAG, which means that outputs from neurons in a layer can connect back to the inputs of neurons in an earlier layer. The storing of outputs and clocking of the whole mess is what keeps it from exploding. These types of networks perform well for processing sequences of inputs, such as those found in handwriting and speech recognition. There’s yet another neural network variation that’s especially good for image processing: the convolutional neural network. You can visualize it as having inputs that are an array of pixel values similar to the convolution kernels that we saw earlier. One big probl

Document: mml-book.txt Distance: 0.27945172786712646
Content: blemathand.Weassumethatourfunctionf isdifferentiable,
andweareunabletoanalyticallyfindasolutioninclosedform.
Gradient descent is a first-order optimization algorithm. To find a local
minimum of a function using gradient descent, one takes steps propor-
tional to the negative of the gradient of the function at the current point.
Weusethe Recall from Section 5.1 that the gradient points in the direction of the
conventionofrow steepest ascent. Another useful intuition is to consider the set of lines
vectorsfor wherethefunctionisatacertainvalue(f(x) = cforsomevaluec R),
gradients. ∈
which are known as the contour lines. The gradient points in a direction
thatisorthogonaltothecontourlinesofthefunctionwewishtooptimize.
Let us consider multivariate functions. Imagine a surface (described by
the function f(x)) with a ball starting at a particular location x . When
0
the ball is released, it will move downhill in the direction of steepest de-
scent.Gradientdescentexploitsthefactthatf(x )decreasesfastestifone
0
movesfr

Document: MathforDeepLearning.txt Distance: 0.30599987506866455
Content:  to minimize the loss function over the training set. That’s the high-level picture. Now let’s make it a little more concrete. Gradients apply to functions that accept vector inputs and return a scalar value. For a neural network, the vector input is the weights and biases, the parameters that define how the network performs once the architecture is fixed. Symbolically, we can write the loss function as L(θ), where θ (theta) is a vector of all the weights and biases in the network. Our goal is to move through the space that the loss function defines to find the minimum, the specific θ leading to the smallest loss, L. We do this by using the gradient of L(θ). Therefore, to train a neural network via gradient descent, we need to know how each weight and bias value contributes to the loss function; that is, we need to know ∂L/∂w, for some weight (or bias) w. Backpropagation is the algorithm that tells us what ∂L/∂w is for each weight and bias of the network. With the partial derivatives, we can apply gradient de

Document: mathandarchitecturesofdeeplearningmeap.txt Distance: 0.31030839475766103
Content: arest minimum) happens along a negative gradient. We can combine several other criteria with the gradient to improve the convergence to the minimum loss value. Each of them results in a different optimization technique: Due to noisy estimations, the local gradient may not always point toward the minimum, but it will have a strong component toward that minimum along with other noisy components. Instead of blindly following the current gradient, we can follow the direction corresponding to a weighted average of the current gradient estimate and the gradient estimate from the previous iteration. This is a recursive process, which effectively means the direction followed at any iteration is a weighted average of the current and all gradient estimates from the beginning of training. Recent gradients are weighted higher, and older gradients are weighed lower. All these gradients have strong components toward the minimum that reinforce each other, while the noisy components point in random directions and tend to can

Document: MathforDeepLearning.txt Distance: 0.33266115188598633
Content: lue contributes to the loss function; that is, we need to know ∂L/∂w, for some weight (or bias) w. Backpropagation is the algorithm that tells us what ∂L/∂w is for each weight and bias of the network. With the partial derivatives, we can apply gradient descent to improve the network’s performance on the next pass of the training data. Before we go any further, a word on terminology. You’ll often hear machine learning folks use backpropagation as a proxy for the entire process of training a neural network. Experienced practitioners understand what they mean, but people new to machine learning are sometimes a bit confused. To be explicit, backpropagation is the algorithm that finds the contribution of each weight and bias value to the network’s error, the ∂L/∂w’s. Gradient descent is the algorithm that uses the ∂L/∂w’s to modify the weights and biases to improve the network’s performance on the training set. Rumelhart, Hinton, and Williams introduced backpropagation in their 1986 paper “Learning Representations
```

```bash
$ python ebook_search.py -q "What is gradient descent?" -b
Found 5 results:
Document: MathforDeepLearning.txt
Distance: 0.5477546957116288

Document: mathandarchitecturesofdeeplearningmeap.txt
Distance: 0.5611605611548662

Document: machinelearningalgorithmsindepth.txt
Distance: 0.5835505324286587

Document: bayesianoptimizationinaction.txt
Distance: 0.6015774845310475

Document: practicalaionthegooglecloudplatform.txt
Distance: 0.6386852939878944
```

```bash
# Out-of-Domain question
python ebook_search.py -q "How do I do a proper squat?"
Found 5 results:
Document: strangecode.txt Distance: 0.632442198250162
Content: to Stance 1 before moving on to the next. Listing 15-10 shows the code for Stance 1 along with the stance itself. MNN5 ! SSSMW ! 5 5SS ! 55555 MNNEE ! 5 5SS ! 5 5 MSE ! 5 5 5WWWWW ! MWWS ! Listing 15-10: Stance 1 With a bit of imagination, you’ll see a figure with outstretched arms. To make the figure dance, we’ll move the arms and legs in sequence. We can move both arms up or down, or move one up and the other down. Similarly, we can move the right leg out or the left leg out for a total of six possible st

Document: Locksport.txt Distance: 0.676541824546943
Content: with tape. Also check whether your cords are a tripping hazard, and if so, hold them down with more tape. Unpack everything else you’ll need and place it on your work area/workbench (see Figure 11-2 for Jos’s typical setup). You can then file a key as a warm-up. This practice will reveal whether you forgot anything and confirm that all your tools are properly connected and placed in the manner you trained for. Figure 11-2: Jos’s typical impressioning setup Round One Round one is the qualifier. At this point

Document: strangecode.txt Distance: 0.6785925818328504
Content: , or move one up and the other down. Similarly, we can move the right leg out or the left leg out for a total of six possible stances. Table 15-1 gives us the code and the appearance of each stance. Table 15-1: The Remaining Stances While developing this example, it was extremely helpful to use the console interpreter in trace mode. I first generated the code for each stance independently of the others. We’ll see below how this helps create the desired animation sequence by literally copying and pasting cod

Document: Locksport.txt Distance: 0.7161288003767967
Content: folding workbench like the one shown in Figure 9-17. These can be purchased fairly inexpensively at most hardware stores, so if you’re traveling for a competition, you can often buy one after you arrive. If you make friends with local competitors, you might even be able to bribe them into storing it for you until next year’s competition too. Figure 9-17: One of Jos’s inexpensive folding workbenches (and Dita) With your own bench, you know exactly what you’re working with, and you can set up exactly the way

Document: Locksport.txt Distance: 0.7198410034179668
Content: n the manner you trained for. Figure 11-2: Jos’s typical impressioning setup Round One Round one is the qualifier. At this point, everybody has their gear set up and is spread out throughout the room. Most competitions supply you with blank keys. Usually, those are the only blanks you’re allowed to use during the competition. Make sure you know the local rules. If you are permitted to use your own blanks, use those since they’re what you trained on. Typically, you’re allowed to put your blank in your grip b
```

### Code

#### Embedding code

```python
import os
import pandas as pd
from db.db_methods import check_db_size, clear_books, create_index, drop_books_table, get_book_text_by_title, init_books_table, initialize_book_embeddings_table, drop_book_embeddings, fast_pg_insert, insert_book, query_similar_books, query_similar_chunks, remove_index, clear_embeddings
from sentence_transformers import SentenceTransformer

# Get the model name from the environment variable
MODEL_NAME = os.getenv('MODEL_NAME', 'all-MiniLM-L6-v2')
CHUNK_LENGTH = int(os.getenv('CHUNK_LENGTH', '500'))
CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', '50'))

def _chunk_text(text, n=500, overlap=50):
    '''
        Split a text into overlapping chunks of length n.

        Parameters:
        text (str): The text to split into chunks.
        n (int): The length of each chunk.
        overlap (int): The number of characters to overlap between chunks.

        Returns:
        List[str]: A list of overlapping text chunks.
    '''
    return [text[i:i+n] for i in range(0, len(text), n-overlap)]

def _process_doc(file_path):
    '''
        Process a document by loading it from disk, splitting it into chunks, and processing each chunk.

        Parameters:
        file_path (str): The path to the file to process.

        Returns:
        List[str]: A list of processed text chunks.
    '''

    text = ''
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    chunks = _chunk_text(text, CHUNK_LENGTH, CHUNK_OVERLAP)
    chunks = [' '.join(chunk.split()) for chunk in chunks]
    return chunks

def _embed_doc(file_path, model, verbose=False):
    '''
        Embed a document by loading it from disk, splitting it into chunks, and embedding each chunk.

        Parameters:
        file_path (str): The path to the file to embed.
        model (SentenceTransformer): The sentence transformer model to use for embedding.

        Returns:
        Tuple[List[str], List[np.array]]: A tuple containing a list of text chunks and a list of chunk embeddings.
    '''
    if verbose:
        print(f'Embedding {file_path}...')
    chunks = _process_doc(file_path)
    return chunks, model.encode(chunks)

def _prepare_doc_for_db(file_path, model, verbose=False):
    '''
        Prepare a document for database insertion by embedding it and creating a DataFrame.

        Parameters:
        file_path (str): The path to the file to process.
        model (SentenceTransformer): The sentence transformer model to use for embedding.

        Returns:
        pd.DataFrame: A DataFrame containing the embeddings and associated metadata.
    '''
    chunks, embeddings = _embed_doc(file_path, model, verbose)
    title = os.path.basename(file_path)

    chunk_offsets = []
    curr_offset = 0
    for chunk in chunks:
        chunk_offsets.append(curr_offset)
        curr_offset += (len(chunk) + 1 - CHUNK_OVERLAP)


    embeddings_list = [embedding.tolist() for embedding in embeddings]

    data = {
        'book_title': [title] * len(chunks),
        'chunk_text': chunks,
        'chunk_number': [int(x) for x in range(1, len(chunks) + 1)],
        'begin_offset': chunk_offsets,
        'embedding': embeddings_list
    }
    return pd.DataFrame(data)

def insert_doc_to_db(file_path, columns=['book_title', 'chunk_text', 'chunk_number', 'begin_offset', 'embedding'], verbose=False):
    '''
        Process a document, prepare it for database insertion, and insert it into the database.

        Parameters:
        file_path (str): The path to the file to process.
        model (SentenceTransformer): The sentence transformer model to use for embedding.
        columns (List[str]): A list of column names in the target table that correspond to the DataFrame columns.

        Returns:
        None
    '''
    if verbose:
        print('Loading model...')
    model = SentenceTransformer(MODEL_NAME)
    if verbose:
        print("Begining insertion process...")
    df = _prepare_doc_for_db(file_path, model, verbose)
    if verbose:
        print("Inserting chunks...")
    title = os.path.basename(file_path)
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    insert_book(title, text)
    fast_pg_insert(df, columns)

def query_database(query, n=5, verbose=False, books=False, extended=False):
    '''
        Query the database for documents containing the given text.

        Parameters:
        query (str): The text to search for in the database.

        Returns:
        List[Tuple[str, str]]: A list of tuples containing the document title and the matching text.
    '''
    if verbose:
        print('Loading model...')
    model = SentenceTransformer(MODEL_NAME)
    if verbose:
        print('Embedding query...')
    query_embedding = model.encode([query])[0].tolist()
    if verbose:
        print('Querying database...')
    if books:
        results = query_similar_books(query_embedding, n)
        results_dict = [{'title': result[0], 'text': 'N/A', 'similarity': result[2]} for result in results]
    elif extended:
        chunk_results = query_similar_chunks(query_embedding, n)
        results_dict = []
        curr_title = ''
        for result in chunk_results:
            if result[0] != curr_title:
                curr_title = result[0]
            book_text = get_book_text_by_title(curr_title)
            offset = result[3]

            start = max(0, offset - CHUNK_LENGTH)
            end = min(len(book_text), offset + CHUNK_LENGTH)

            results_dict.append({'title': result[0], 'text': book_text[start:end], 'similarity': result[2]})
    else:
        results = query_similar_chunks(query_embedding, n)
        results_dict = [{'title': result[0], 'text': result[1], 'similarity': result[2]} for result in results]

    return results_dict

def init_table():
    '''
        Initialize the database by creating the table for document embeddings.

        Parameters:
        None

        Returns:
        None
    '''
    print('Creating tables...')
    init_books_table()
    initialize_book_embeddings_table()
    print('Tables created.')

def init_index():
    '''
        Initialize the database index for the embeddings column.

        Parameters:
        None

        Returns:
        None
    '''
    print('Creating index...')
    create_index()
    print('Index created.')

def reindex():
    '''
        Recreate the database index for the embeddings column.

        Parameters:
        None

        Returns:
        None
    '''
    print('Recreating index...')
    remove_index()
    create_index()
    print('Index recreated.')

def clear_db():
    '''
        Clear the PostgreSQL table of all data.

        Parameters:
        None

        Returns:
        None
    '''
    print('Clearing database...')
    remove_index()
    clear_embeddings()
    clear_books()
    print('Database cleared.')

def delete_table():
    '''
        Drop the PostgreSQL table for storing book embeddings.

        Parameters:
        None

        Returns:
        None
    '''
    print('Dropping tables...')
    drop_book_embeddings()
    drop_books_table()
    print('Tables dropped.')

def get_database_size():
    '''
        Get the size of the database in a human-readable format.

        Parameters:
        None

        Returns:
        str: The size of the database.
    '''
    print('Querying database size...')
    return check_db_size()
```

#### Vector DB Code

```python
import io
import os
import pandas as pd
import psycopg2

from typing import List

from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv('CONNECTION_STRING', "postgresql://nlp_user:nlp_password@localhost:6012/nlp_db")
EMBEDDING_LENGTH = os.getenv('EMBEDDING_LENGTH', 384)

CREATE_EXTENSION = "CREATE EXTENSION IF NOT EXISTS vector;"

INITIALIZE_BOOK_EMBEDDINGS_TABLE = f'''
                CREATE TABLE IF NOT EXISTS book_embeddings (
                    id SERIAL PRIMARY KEY,
                    book_title TEXT,
                    chunk_text TEXT,
                    chunk_number INTEGER,
                    begin_offset INTEGER,
                    embedding vector({EMBEDDING_LENGTH}),
                    FOREIGN KEY (book_title) REFERENCES books(title)
                );
                '''

DROP_BOOK_EMBEDDINGS = "DROP TABLE IF EXISTS book_embeddings;"

CREATE_INDEX = '''
                CREATE INDEX IF NOT EXISTS embedding_idx ON book_embeddings
                USING hnsw (embedding vector_cosine_ops)
                WITH (m = 16, ef_construction = 64);
                '''

REMOVE_INDEX = "DROP INDEX IF EXISTS embedding_idx;"

INSERT_DOC = '''
             INSERT INTO book_embeddings (book_title, chunk_text, chunk_number, begin_offset, embedding)
             VALUES (%s, %s, %s, %s, %s);
             '''

QUERY_SIMILAR_CHUNKS = '''
                        SELECT book_title, chunk_text, embedding <=> %s::vector AS distance, begin_offset
                        FROM book_embeddings
                        ORDER BY distance
                        LIMIT %s;
                        '''

QUERY_SIMILAR_BOOKS = '''
                        SELECT book_title, AVG(embedding) AS avg_embedding, AVG(embedding) <=> %s::vector AS distance
                        FROM book_embeddings
                        GROUP BY book_title
                        ORDER BY distance
                        LIMIT %s;
                        '''

CLEAR_ALL_EMBEDDINGS = "DELETE FROM book_embeddings;"

CHECK_DB_SIZE = 'SELECT pg_size_pretty(pg_database_size(current_database()));'

CREATE_BOOKS_TABLE = '''
                    CREATE TABLE IF NOT EXISTS books (
                        id SERIAL PRIMARY KEY,
                        title TEXT UNIQUE,
                        text TEXT
                    );
                    '''

INSERT_BOOK = '''
                INSERT INTO books (title, text)
                VALUES (%s, %s)
                ON CONFLICT (title) DO NOTHING;
                '''

CLEAR_BOOKS = "DELETE FROM books;"

DROP_BOOKS = "DROP TABLE IF EXISTS books;"

GET_BOOK_TEXT_BY_TITLE = "SELECT text FROM books WHERE title = %s;"

def initialize_book_embeddings_table():
    '''
        Create the PostgreSQL table for storing book embeddings.

        Parameters:
        None

        Returns:
        None
    '''

    with psycopg2.connect(CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_EXTENSION)
            cursor.execute(INITIALIZE_BOOK_EMBEDDINGS_TABLE)
            connection.commit()

def drop_book_embeddings():
    '''
        Drop the PostgreSQL table for storing book embeddings.

        Parameters:
        None

        Returns:
        None
    '''

    with psycopg2.connect(CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            cursor.execute(DROP_BOOK_EMBEDDINGS)
            connection.commit()

def create_index():
    '''
        Create the PostgreSQL index for the book embeddings.

        Parameters:
        None

        Returns:
        None
    '''

    with psycopg2.connect(CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_INDEX)
            connection.commit()

def remove_index():
    '''
        Remove the PostgreSQL index for the book embeddings.

        Parameters:
        None

        Returns:
        None
    '''

    with psycopg2.connect(CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            cursor.execute(REMOVE_INDEX)
            connection.commit()

def clear_embeddings():
    '''
        Clear the PostgreSQL table of all data.

        Parameters:
        None

        Returns:
        None
    '''

    with psycopg2.connect(CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            cursor.execute(CLEAR_ALL_EMBEDDINGS)
            connection.commit()

def insert_chunk(book_title, chunk_text, chunk_number, begin_offset, embedding):
    '''
        Insert a document chunk into the PostgreSQL database.

        Parameters:
        book_title (str): The title of the book.
        chunk_text (str): The text of the chunk.
        chunk_number (int): The chunk number within the chapter.
        embedding (np.array): The embedding of the chunk.

        Returns:
        None
    '''
    # Convert types before insertion
    chunk_number = int(chunk_number)  # Convert np.int64 to Python int


    with psycopg2.connect(CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(INSERT_DOC, (book_title, chunk_text, chunk_number, begin_offset, embedding))
                connection.commit()
                print(f"Successfully inserted chunk {chunk_number}")
            except Exception as e:
                print(f"Error inserting chunk: {e}")
                print(f"Types: book_title={type(book_title)}, chunk_text={type(chunk_text)}, "
                      f"chunk_number={type(chunk_number)}, embedding={type(embedding)}")
                connection.rollback()
                raise

def fast_pg_insert(df: pd.DataFrame, columns: List[str]) -> None:
    """
        Inserts data from a pandas DataFrame into a PostgreSQL table using the COPY command for fast insertion.

        Parameters:
        df (pd.DataFrame): The DataFrame containing the data to be inserted.
        connection (str): The connection string to the PostgreSQL database.
        table_name (str): The name of the target table in the PostgreSQL database.
        columns (List[str]): A list of column names in the target table that correspond to the DataFrame columns.

        Returns:
        None
    """
    conn = psycopg2.connect(CONNECTION_STRING)
    _buffer = io.StringIO()
    df.to_csv(
        _buffer,
        sep='\t',          # Use tab as separator instead of semicolon
        index=False,
        header=False,
        escapechar='\\',   # Add escape character
        doublequote=True,  # Handle quotes properly
        na_rep='\\N'       # Proper NULL handling
    )
    _buffer.seek(0)
    with conn.cursor() as c:
        c.copy_from(
                file=_buffer,
                table='book_embeddings',
                sep='\t',              # Match the separator used in to_csv
                columns=columns,
                null='\\N'            # Match the null representation
            )
    conn.commit()
    conn.close()

def query_similar_chunks(embedding, top_n=5):
    '''
        Query the PostgreSQL database for similar embeddings.

        Parameters:
        embedding (np.array): The embedding to query for.
        top_n (int): The number of similar embeddings to return.

        Returns:
        List: A list of similar embeddings.
    '''

    with psycopg2.connect(CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            cursor.execute(QUERY_SIMILAR_CHUNKS, (embedding, top_n))
            results = cursor.fetchall()

    return results

def query_similar_books(embedding, top_n=5):
    '''
        Query the PostgreSQL database for similar books.

        Parameters:
        embedding (np.array): The embedding to query for.
        top_n (int): The number of similar books to return.

        Returns:
        List: A list of similar books.
    '''

    with psycopg2.connect(CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            cursor.execute(QUERY_SIMILAR_BOOKS, (embedding, top_n))
            results = cursor.fetchall()

    return results

def check_db_size():
    '''
        Check the size of the PostgreSQL database.

        Parameters:
        None

        Returns:
        str: The size of the database in human-readable format.
    '''

    with psycopg2.connect(CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            cursor.execute(CHECK_DB_SIZE)
            size = cursor.fetchone()[0]

    return size

def init_books_table():
    '''
        Create the PostgreSQL table for storing book texts.

        Parameters:
        None

        Returns:
        None
    '''

    with psycopg2.connect(CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_BOOKS_TABLE)
            connection.commit()

def insert_book(title, text):
    '''
        Insert a book into the PostgreSQL database.

        Parameters:
        title (str): The title of the book.
        text (str): The text of the book.

        Returns:
        None
    '''

    with psycopg2.connect(CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_BOOK, (title, text))
            connection.commit()

def clear_books():
    '''
        Clear the PostgreSQL table of all books.

        Parameters:
        None

        Returns:
        None
    '''

    with psycopg2.connect(CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            cursor.execute(CLEAR_BOOKS)
            connection.commit()

def drop_books_table():
    '''
        Drop the PostgreSQL table for storing book texts.

        Parameters:
        None

        Returns:
        None
    '''

    with psycopg2.connect(CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            cursor.execute(DROP_BOOKS)
            connection.commit()

def get_book_text_by_title(title):
    '''
        Retrieve the text of a book from the PostgreSQL database.

        Parameters:
        title (str): The title of the book.

        Returns:
        str: The text of the book.
    '''

    with psycopg2.connect(CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_BOOK_TEXT_BY_TITLE, (title,))
            text = cursor.fetchone()[0]

    return text
```
