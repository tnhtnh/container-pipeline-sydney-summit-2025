package main

import (
        "encoding/json"
        "fmt"
        "log"
        "net/http"
        "os"
        "os/exec"
)

// Response structs for JSON responses
type MessageResponse struct {
        Message string `json:"message"`
}

type StatusResponse struct {
        Status string `json:"status"`
}

type CommandResponse struct {
        Result string `json:"result"`
}

// CommandRequest struct for parsing JSON requests
type CommandRequest struct {
        Command string `json:"command"`
}

func main() {
        // Register route handlers
        http.HandleFunc("/", indexHandler)
        http.HandleFunc("/healthcheck", healthcheckHandler)
        http.HandleFunc("/summit", summitHandler)
        http.HandleFunc("/run_command", runCommandHandler)

        // Start the server
        port := 80
        fmt.Printf("Server starting on port %d...\n", port)
        log.Fatal(http.ListenAndServe(fmt.Sprintf(":%d", port), nil))
}

// indexHandler returns a JSON message with the git SHA
func indexHandler(w http.ResponseWriter, r *http.Request) {
        gitSHA := os.Getenv("GIT_SHA")
        if gitSHA == "" {
                gitSHA = "unknown"
        }

        response := MessageResponse{
                Message: fmt.Sprintf("Application version: %s", gitSHA),
        }

        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(response)
}

// healthcheckHandler returns a status OK
func healthcheckHandler(w http.ResponseWriter, r *http.Request) {
        response := StatusResponse{
                Status: "OK",
        }

        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(response)
}

// summitHandler returns a specific message
func summitHandler(w http.ResponseWriter, r *http.Request) {
        response := MessageResponse{
                Message: "I hope you are enjoying this talk",
        }

        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(response)
}

// Variable to allow mocking exec.Command in tests
var execCommand = exec.Command

// runCommandHandler executes shell commands from user input
// SECURITY VULNERABILITY: Command Injection
// This endpoint executes shell commands from user input without validation,
// creating a command injection vulnerability.
func runCommandHandler(w http.ResponseWriter, r *http.Request) {
        // Only allow POST requests
        if r.Method != http.MethodPost {
                http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
                return
        }

        // Parse the JSON request
        var req CommandRequest
        if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
                http.Error(w, "Invalid request body", http.StatusBadRequest)
                return
        }

        // Vulnerable code: directly executing user input
        cmd := execCommand("sh", "-c", req.Command)
        output, err := cmd.CombinedOutput()
        if err != nil {
                http.Error(w, fmt.Sprintf("Command execution failed: %v", err), http.StatusInternalServerError)
                return
        }

        // Return the command output
        response := CommandResponse{
                Result: string(output),
        }

        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(response)
}