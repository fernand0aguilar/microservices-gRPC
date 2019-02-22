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
	"strconv"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"

	pb "microservices-grpc/service02_products_listing/hashtest"
)

func getDiscountConnection(host string) (*grpc.ClientConn, error) {
	wd, _ := os.Getwd()
	parentDir := filepath.Dir(wd)
	certFile := filepath.Join(parentDir, "keys", "cert.pem")
	creds, _ := credentials.NewClientTLSFromFile(certFile, "")
	return grpc.Dial(host, grpc.WithTransportCredentials(creds))
}

func findUserByID(id int) (pb.User, error) {
	c1 := pb.User{Id: "1", FirstName: "John", LastName: "Snow"}
	c2 := pb.User{Id: "2", FirstName: "Daenerys", LastName: "Targaryen"}
	users := map[int]pb.User{
		1: c1,
		2: c2,
	}
	found, ok := users[id]
	if ok {
		return found, nil
	}
	return found, errors.New("User not found.")
}

func getFakeProducts() []*pb.Product {
	p1 := pb.Product{Id: "1", PriceInCents: 99999, Title: "iphone-x", Description: "64GB, black and iOS 12"}
	p2 := pb.Product{Id: "2", PriceInCents: 150000, Title: "notebook-avell-g1511", Description: "Notebook Gamer Intel Core i7"}
	p3 := pb.Product{Id: "3", PriceInCents: 32999, Title: "playstation-4-slim", Description: "1TB Console"}
	return []*pb.Product{&p1, &p2, &p3}
}

func getProductsWithDiscountApplied(user pb.User, products []*pb.Product) []*pb.Product {
	host := os.Getenv("DISCOUNT_SERVICE_HOST")
	if len(host) == 0 {
		host = "localhost:11443"
	}
	conn, err := getDiscountConnection(host)
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()

	c := pb.NewDiscountClient(conn)
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*10)
	defer cancel()

	productsWithDiscountApplied := make([]*pb.Product, 0)
	for _, product := range products {
		r, err := c.ApplyDiscount(ctx, &pb.DiscountRequest{User: &user, Product: product})
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
	id, err := strconv.Atoi(userID)
	if err != nil {
		http.Error(w, "User ID is not a number.", http.StatusBadRequest)
		return
	}

	user, err := findUserByID(id)
	if err != nil {
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

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "It is working.")
	})
	http.HandleFunc("/products", handleGetProducts)

	fmt.Println("Server running on", port)
	http.ListenAndServe(":"+port, nil)
}
