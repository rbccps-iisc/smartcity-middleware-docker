// Copyright (C) 2013 Chen "smallfish" Xiaoyu (陈小玉)
// Updated 2018 by Poorna Chandra Tejasvi, RBCCPS, Indian Institute of Science (ver.0.1.0)
package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"github.com/streadway/amqp"
	"io/ioutil"
	"log"
	"net/http"
	"time"
)

var (
	address = flag.String("address", "0.0.0.0:8000", "bind host:port")
)

var request *http.Request

func init() {
	flag.Parse()
}

// Entity for HTTP Request Body: Message/Exchange/Queue/QueueBind JSON Input
type MessageEntity struct {
	Exchange     string `json:"exchange"`
	Key          string `json:"key"`
	DeliveryMode uint8  `json:"deliverymode"`
	Priority     uint8  `json:"priority"`
	Body         string `json:"body"`
}

type ExchangeEntity struct {
	Name       string `json:"name"`
	Type       string `json:"type"`
	Durable    bool   `json:"durable"`
	AutoDelete bool   `json:"autodelete"`
	NoWait     bool   `json:"nowait"`
}

type QueueEntity struct {
	Name       string `json:"name"`
	Durable    bool   `json:"durable"`
	AutoDelete bool   `json:"autodelete"`
	Exclusive  bool   `json:"exclusive"`
	NoWait     bool   `json:"nowait"`
}

type QueueBindEntity struct {
	Queue    string   `json:"queue"`
	Exchange string   `json:"exchange"`
	NoWait   bool     `json:"nowait"`
	Key     []string `json:"key"` // bind/routing keys
}

// RabbitMQ Operate Wrapper
type RabbitMQ struct {
	conn    *amqp.Connection
	channel *amqp.Channel
	done    chan error
}


func (r *RabbitMQ) Connect() (err error) {
	r.conn, err = amqp.Dial("amqp://" + request.Header.Get("X-Consumer-Username") + ":" + request.Header.Get("Apikey") + "@localhost:5672/")
	if err != nil {
		log.Printf(request.Header.Get("X-Real-Ip")+" "+request.Header.Get("X-Consumer-Id")+" "+request.Header.Get("X-Consumer-Username")+" "+request.Header.Get("Apikey")+" [amqp] connect error: %s\n", err)
		return err
	}
	r.channel, err = r.conn.Channel()
	if err != nil {
		log.Printf(request.Header.Get("X-Real-Ip")+" "+request.Header.Get("X-Consumer-Id")+" "+request.Header.Get("X-Consumer-Username")+" "+request.Header.Get("Apikey")+" [amqp] get channel error: %s\n", err)
		return err
	}
	r.done = make(chan error)
	return nil
}




func (r *RabbitMQ) Publish(exchange, key string, deliverymode, priority uint8, body string) (err error) {

	err = r.channel.Publish(exchange, key, false, false,
		amqp.Publishing{
			Headers:         amqp.Table{},
			ContentType:     "text/plain",
			ContentEncoding: "",
			DeliveryMode:    deliverymode,
			Priority:        priority,
			Body:            []byte(body),
		},
	)



	if err != nil {
		log.Printf(request.Header.Get("X-Real-Ip")+" "+request.Header.Get("X-Consumer-Id")+" "+request.Header.Get("X-Consumer-Username")+" "+request.Header.Get("Apikey")+" [amqp] publish message error: %s\n", err)
		return err
	}
	return nil
}

func (r *RabbitMQ) DeclareExchange(name, typ string, durable, autodelete, nowait bool) (err error) {
	err = r.channel.ExchangeDeclare(name, typ, durable, autodelete, false, nowait, nil)
	if err != nil {
		log.Printf(request.Header.Get("X-Real-Ip")+" "+request.Header.Get("X-Consumer-Id")+" "+request.Header.Get("X-Consumer-Username")+" "+request.Header.Get("Apikey")+" [amqp] declare exchange error: %s\n", err)
		return err
	}
	return nil
}

func (r *RabbitMQ) DeleteExchange(name string) (err error) {
	err = r.channel.ExchangeDelete(name, false, false)
	if err != nil {
		log.Printf(request.Header.Get("X-Real-Ip")+" "+request.Header.Get("X-Consumer-Id")+" "+request.Header.Get("X-Consumer-Username")+" "+request.Header.Get("Apikey")+" [amqp] delete exchange error: %s\n", err)
		return err
	}
	return nil
}

func (r *RabbitMQ) DeclareQueue(name string, durable, autodelete, exclusive, nowait bool) (err error) {
	_, err = r.channel.QueueDeclare(name, durable, autodelete, exclusive, nowait, nil)
	if err != nil {
		log.Printf(request.Header.Get("X-Real-Ip")+" "+request.Header.Get("X-Consumer-Id")+" "+request.Header.Get("X-Consumer-Username")+" "+request.Header.Get("Apikey")+" [amqp] declare queue error: %s\n", err)
		return err
	}
	return nil
}

func (r *RabbitMQ) DeleteQueue(name string) (err error) {
	// TODO: other property wrapper
	_, err = r.channel.QueueDelete(name, false, false, false)
	if err != nil {
		log.Printf(request.Header.Get("X-Real-Ip")+" "+request.Header.Get("X-Consumer-Id")+" "+request.Header.Get("X-Consumer-Username")+" "+request.Header.Get("Apikey")+" [amqp] delete queue error: %s\n", err)
		return err
	}
	return nil
}

func (r *RabbitMQ) BindQueue(queue, exchange string, keys []string, nowait bool) (err error) {

	for _, key := range keys {
		if err = r.channel.QueueBind(queue, key, exchange, nowait, nil); err != nil {
			log.Printf(request.Header.Get("X-Real-Ip")+" "+request.Header.Get("X-Consumer-Id")+" "+request.Header.Get("X-Consumer-Username")+" "+request.Header.Get("Apikey")+" [amqp] bind queue error: %s\n", err)
			return err
		}
	}
	return nil
}

func (r *RabbitMQ) UnBindQueue(queue, exchange string, keys []string) (err error) {
	for _, key := range keys {
		if err = r.channel.QueueUnbind(queue, key, exchange, nil); err != nil {
			log.Printf(request.Header.Get("X-Real-Ip")+" "+request.Header.Get("X-Consumer-Id")+" "+request.Header.Get("X-Consumer-Username")+" "+request.Header.Get("Apikey")+" [amqp] unbind queue error: %s\n", err)
			return err
		}
	}
	return nil
}

func (r *RabbitMQ) ConsumeQueue(queue string, message chan []byte) (err error) {
	deliveries, err := r.channel.Consume(queue, "", true, false, false, false, nil)
	if err != nil {
		log.Printf(request.Header.Get("X-Real-Ip")+" "+request.Header.Get("X-Consumer-Id")+" "+request.Header.Get("X-Consumer-Username")+" "+request.Header.Get("Apikey")+" [amqp] consume queue error: %s\n", err)
		return err
	}
	go func(deliveries <-chan amqp.Delivery, done chan error, message chan []byte) {
		for d := range deliveries {
			message <- d.Body
			log.Printf(request.Header.Get("X-Real-Ip")+" "+request.Header.Get("X-Consumer-Id")+" "+request.Header.Get("X-Consumer-Username")+" "+request.Header.Get("Apikey")+" Sending Content in Queue Now")
		}
		done <- nil
	}(deliveries, r.done, message)
	log.Printf(request.Header.Get("X-Real-Ip")+" "+request.Header.Get("X-Consumer-Id")+" "+request.Header.Get("X-Consumer-Username")+" "+request.Header.Get("Apikey")+" Queue is Empty Now")
	return nil
}

func (r *RabbitMQ) Close() (err error) {
	err = r.conn.Close()
	if err != nil {
		log.Printf(request.Header.Get("X-Real-Ip")+" "+request.Header.Get("X-Consumer-Id")+" "+request.Header.Get("X-Consumer-Username")+" "+request.Header.Get("Apikey")+" [amqp] close error: %s\n", err)
		return err
	}
	return nil
}

// HTTP Handlers
func QueueHandler(w http.ResponseWriter, r *http.Request) {

	request=r
	if r.Method == "POST" || r.Method == "DELETE" {
		body, err := ioutil.ReadAll(r.Body)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		entity := new(QueueEntity)
		if err = json.Unmarshal(body, entity); err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		rabbit := new(RabbitMQ)
		if err = rabbit.Connect(); err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		defer rabbit.Close()

		if r.Method == "POST" {
			if err = rabbit.DeclareQueue(entity.Name, entity.Durable, entity.AutoDelete, entity.Exclusive, entity.NoWait); err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
				return
			}
			w.Write([]byte("Declare queue OK\n"))
		} else if r.Method == "DELETE" {
			if err = rabbit.DeleteQueue(entity.Name); err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
				return
			}
			w.Write([]byte("Delete queue OK\n"))
		}
	} else if r.Method == "GET" {
		r.ParseForm()

		log.Printf(r.Header.Get("X-Real-Ip")+" "+r.Header.Get("X-Consumer-Id")+" "+r.Header.Get("X-Consumer-Username")+" "+r.Header.Get("Apikey")+" In GET QueueHandler Now")
		rabbit := new(RabbitMQ)
		if err := rabbit.Connect(); err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		log.Printf(r.Header.Get("X-Real-Ip")+" "+r.Header.Get("X-Consumer-Id")+" "+r.Header.Get("X-Consumer-Username")+" "+r.Header.Get("Apikey")+" Connecting to the Queue")

		message := make(chan []byte)

		for _, name := range r.Form["name"] {
			log.Printf(request.Header.Get("X-Real-Ip")+" "+request.Header.Get("X-Consumer-Id")+" "+request.Header.Get("X-Consumer-Username")+" "+request.Header.Get("Apikey")+" Got {%v}", name)
			if err := rabbit.ConsumeQueue(name, message); err != nil {
				log.Printf(request.Header.Get("X-Real-Ip")+" "+request.Header.Get("X-Consumer-Id")+" "+request.Header.Get("X-Consumer-Username")+" "+request.Header.Get("Apikey")+" Connection Closed")
				http.Error(w, err.Error(), http.StatusInternalServerError)
				return
			}
		}

		w.Write([]byte(""))
		w.(http.Flusher).Flush()
		name := r.Form["name"]

		// Check the status of the Connection and Close the Queue Here //
		notify := w.(http.CloseNotifier).CloseNotify()
		go func() {
			<-notify
			log.Printf(r.Header.Get("X-Real-Ip")+" "+r.Header.Get("X-Consumer-Id")+" "+r.Header.Get("X-Consumer-Username")+" "+r.Header.Get("Apikey")+" HTTP connection just closed for {%v}", name)
			rabbit.Close()
			log.Printf(r.Header.Get("X-Real-Ip")+" "+r.Header.Get("X-Consumer-Id")+" "+r.Header.Get("X-Consumer-Username")+" "+r.Header.Get("Apikey")+" AMQP connection is now closed for {%v}", name)
		}()

		for {
			fmt.Fprintf(w, "%s\n", <-message)
			w.(http.Flusher).Flush()
			log.Printf(r.Header.Get("X-Real-Ip")+" "+r.Header.Get("X-Consumer-Id")+" "+r.Header.Get("X-Consumer-Username")+" "+r.Header.Get("Apikey")+" Sending data to Client {%v}", name)
		}

		rabbit.Close()

	} else {
		w.WriteHeader(http.StatusMethodNotAllowed)
	}
}

func QueueBindHandler(w http.ResponseWriter, r *http.Request) {

	request=r
	if r.Method == "POST" || r.Method == "DELETE" {
		body, err := ioutil.ReadAll(r.Body)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		entity := new(QueueBindEntity)
		if err = json.Unmarshal(body, entity); err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		rabbit := new(RabbitMQ)
		if err = rabbit.Connect(); err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		defer rabbit.Close()

		if r.Method == "POST" {

			//entity.Exchange = entity.Key[0] + ".protected"
			//entity.Queue = request.Header.Get("X-Consumer-Username")
			if err = rabbit.BindQueue(entity.Queue, entity.Exchange, entity.Key, entity.NoWait); err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
				return
			}
			w.Write([]byte("Bind queue OK\n"))
		} else if r.Method == "DELETE" {
                        //entity.Exchange = entity.Key[0] + ".protected"
                        //entity.Queue = request.Header.Get("X-Consumer-Username")
			if err = rabbit.UnBindQueue(entity.Queue, entity.Exchange, entity.Key); err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
				return
			}
			w.Write([]byte("Unbind queue OK\n"))
		}
	} else {
		w.WriteHeader(http.StatusMethodNotAllowed)
	}
}

func PublishHandler(w http.ResponseWriter, r *http.Request) {

	request=r
	cFail := make(chan amqp.Return,	1)

	if r.Method == "POST" {
		body, err := ioutil.ReadAll(r.Body)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		entity := new(MessageEntity)
		if err = json.Unmarshal(body, entity); err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		rabbit := new(RabbitMQ)
		if err = rabbit.Connect(); err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		defer rabbit.Close()
		if entity.Exchange == "" { entity.Exchange = request.Header.Get("X-Consumer-Username") + ".protected" }
		if entity.Key == "" { entity.Key = request.Header.Get("X-Consumer-Username") }
//entity.Exchange = request.Header.Get("X-Consumer-Username") + ".protected"
        //entity.Key = request.Header.Get("X-Consumer-Username")
		if err = rabbit.Publish(entity.Exchange, entity.Key, entity.DeliveryMode, entity.Priority, entity.Body); err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		rabbit.channel.NotifyReturn(cFail)

		select
		{
		case ch:=<-cFail:
			log.Printf(r.Header.Get("X-Real-Ip")+" "+r.Header.Get("X-Consumer-Id")+" "+r.Header.Get("X-Consumer-Username")+" "+r.Header.Get("Apikey")+" Incorrect exchange or queue name")
			http.Error(w,"Incorrect exchange or queue name "+ch.ReplyText,http.StatusNotFound)
			return

		case <- time.After(100*time.Millisecond):
			w.Write([]byte("Publish message OK\n"))
			return
		}

// 		select
// 		{
// 		case ch:=<-cFail:
// 			log.Printf(r.Header.Get("X-Real-Ip")+" "+r.Header.Get("X-Consumer-Id")+" "+r.Header.Get("X-Consumer-Username")+" "+r.Header.Get("Apikey")+" Incorrect exchange or queue name")
// 			http.Error(w,"Incorrect exchange or queue name "+ch.ReplyText,http.StatusNotFound)
// 			return

// 		default:
// 			w.Write([]byte("Publish message OK\n"))
// 			return
// 		}



	} else {
		w.WriteHeader(http.StatusMethodNotAllowed)
		return
	}
}

func ExchangeHandler(w http.ResponseWriter, r *http.Request) {

	request=r
	if r.Method == "POST" || r.Method == "DELETE" {
		body, err := ioutil.ReadAll(r.Body)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		entity := new(ExchangeEntity)
		if err = json.Unmarshal(body, entity); err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		rabbit := new(RabbitMQ)
		if err = rabbit.Connect(); err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		defer rabbit.Close()

		if r.Method == "POST" {
			if err = rabbit.DeclareExchange(entity.Name, entity.Type, entity.Durable, entity.AutoDelete, entity.NoWait); err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
				return
			}
			w.Write([]byte("Declare exchange OK\n"))
		} else if r.Method == "DELETE" {
			if err = rabbit.DeleteExchange(entity.Name); err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
				return
			}
			w.Write([]byte("Delete exchange OK"))
		}
	} else {
		w.WriteHeader(http.StatusMethodNotAllowed)
	}
}

func main() {
	// Register HTTP Handlers
	http.HandleFunc("/exchange", ExchangeHandler)
	http.HandleFunc("/queue/bind", QueueBindHandler)
	http.HandleFunc("/queue", QueueHandler)
	http.HandleFunc("/publish", PublishHandler)

	// Start HTTP Server
	log.Printf("server run %s \n", *address)
	err := http.ListenAndServe(*address, nil)
	if err != nil {
		log.Fatal(err)
	}
}