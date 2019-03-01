package main

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"

	protobuf "microservices-grpc/products_listing/hashtest"
)

func getDiscountConnection(host string) (*grpc.ClientConn, error) {
	// Dial TLS Connection
	wd, _ := os.Getwd()
	parentDir := filepath.Dir(wd)
	certFile := filepath.Join(parentDir, "keys", "cert.pem")
	creds, _ := credentials.NewClientTLSFromFile(certFile, "")
	return grpc.Dial(host, grpc.WithTransportCredentials(creds))
}

func findUserByID(id string) (protobuf.User, error) {
	user1 := protobuf.User{
		Id: "1", 
		FirstName: "John", 
		LastName: "Snow", 
		DateOfBirth: "23021997",
	}
	user2 := protobuf.User{
		Id: "2", 
		FirstName: "Daenerys", 
		LastName: "Targaryen",
		DateOfBirth: "05021997",
	}

	users := map[string]protobuf.User{
		"1": user1,
		"2": user2,
	}
	found, ok := users[id]
	
	if ok {
		// log.Println("FOUND user with id + " + id)
		return found, nil
	}
	return found, errors.New("User not found.")
}

func getFakeProducts() []*protobuf.Product {
	p1 := protobuf.Product{Id: "1", PriceInCents: 99999, 
		Title: "iphone-x", 
		Description: "64GB, black and iOS 12"}
	p2 := protobuf.Product{Id: "2", PriceInCents: 150000, 
		Title: "notebook-avell-g1511",
		Description: "Notebook Gamer Intel Core i7"}
	p3 := protobuf.Product{Id: "3", PriceInCents: 32999, 
		Title: "playstation-4-slim", 
		Description: "1TB Console"}
	
	return []*protobuf.Product{&p1, &p2, &p3}
}

func getProductsWithDiscountApplied(user protobuf.User, products []*protobuf.Product) []*protobuf.Product {
	host := os.Getenv("DISCOUNT_SERVICE_HOST")
	if len(host) == 0 {
		host = "localhost:11443"
	}
	conn, err := getDiscountConnection(host)

	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()

	client := protobuf.NewDiscountClient(conn)
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*10)
	defer cancel()

	productsWithDiscountApplied := make([]*protobuf.Product, 0)
	for _, product := range products {
		r, err := client.ApplyDiscount(ctx, &protobuf.DiscountRequest{User: &user, Product: product})
		if err == nil {
			productsWithDiscountApplied = append(productsWithDiscountApplied, r.GetProduct())
		} else {
			log.Println("Failed to apply discount.", err)
		}
	}

	if len(productsWithDiscountApplied) > 0 {
		return productsWithDiscountApplied
	}
	return products
}

func handleGetProducts(w http.ResponseWriter, req *http.Request) {
	products := getFakeProducts()
	w.Header().Set("Content-Type", "application/json")

	userID := req.Header.Get("X-USER-ID")
	if userID == "" {
		json.NewEncoder(w).Encode(products)
		return
	}
	log.Println("userID: "+ userID)

	user, err := findUserByID(userID)
	if err != nil {
		log.Println("error: ", err )
		json.NewEncoder(w).Encode(products)
		return
	}

	productsWithDiscountApplied := getProductsWithDiscountApplied(user, products)
	json.NewEncoder(w).Encode(productsWithDiscountApplied)
}

func main() {
	port := "11080"
	if len(os.Args) > 1 {
		port = os.Args[1]
	}
	fmt.Println("Server is running on", port)
	http.HandleFunc("/products", handleGetProducts)	
	http.ListenAndServe(":" + port, nil)
}
