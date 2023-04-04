package main

import (
	"database/sql"
	"fmt"
	"log"
	"os/exec"

	"github.com/gin-contrib/static"
	"github.com/gin-gonic/gin"
	_ "github.com/mattn/go-sqlite3"
)

func main() {

	DB_STRING := "Z:\\other\\spotify_backup.db"
	// DB_STRING := "Z:\\other\\spotify_backup_backup.db"

	fmt.Println("hello world")

	// db connect
	db, err := sql.Open("sqlite3", DB_STRING)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	var version string
	err = db.QueryRow("SELECT SQLITE_VERSION()").Scan(&version)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(version)

	r := gin.Default()
	r.Use(static.Serve("/", static.LocalFile("./client/dist/", false)))

	r.GET("/ping", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"message": "pong",
		})
	})

	type Track struct {
		Track_uri   string
		Track_name  string
		Artist_uri  string
		Artist_name string
		Album_uri   string
		Album_name  string
		Duration_ms int
	}

	r.GET("/sql", func(c *gin.Context) {
		var track Track
		err = db.QueryRow("SELECT * FROM tracks LIMIT 1;").Scan(&track.Track_uri, &track.Track_name, &track.Artist_uri, &track.Artist_name, &track.Album_uri, &track.Album_name, &track.Duration_ms)
		if err != nil {
			log.Fatal(err)
		}
		c.JSONP(200, track)
	})

	r.GET("/gencaselist/:seed_track", func(c *gin.Context) {
		seed_track := c.Param("seed_track")
		fmt.Println("generating case-based list off " + seed_track + "...")
		cmd := exec.Command("python", "-c", "import case; print(case.main('"+seed_track+"'), end='')")
		fmt.Println(cmd.Args)
		out, err := cmd.CombinedOutput()
		if err != nil {
			fmt.Println(err)
			c.AbortWithError(500, err)
		}
		fmt.Println(string(out))
		c.JSON(200, gin.H{
			"output": string(out),
		})
	})

	r.GET("/search/:name", func(c *gin.Context) {
		name := c.Param("name")
		var tracks []Track
		stmt, err := db.Prepare("SELECT * FROM tracks WHERE track_name LIKE %?% LIMIT 20;")
		if err != nil {
			log.Fatal(err)
		}
		rows, err := stmt.Query(name)
		if err != nil {
			c.AbortWithStatus(500)
		}
		defer rows.Close()
		for rows.Next() {
			var track Track
			if err := rows.Scan(&track.Track_uri, &track.Track_name, &track.Artist_uri, &track.Artist_name, &track.Album_uri, &track.Album_name, &track.Duration_ms); err != nil {
				log.Fatal(err)
			}
			tracks = append(tracks, track)
		}
		if err = rows.Err(); err != nil {
			log.Fatal(err)
		}
		c.JSONP(200, tracks)
	})

	r.Run("localhost:4000") // listen and serve on 0.0.0.0:8080
}

// func test() {
// 	dsn := flag.String("dsn", os.Getenv("DSN"), "connection data source name")
// 	db, err := sql.Open("driver-name", *dsn)
// }

// func test2() {
// 	sql.Register("sqlite3_with_hook_example",
// 		&sqlite3.SQLiteDriver{
// 			ConnectHook: func(conn *sqlite3.SQLiteConn) error {
// 				sqlite3conn = append(sqlite3conn, conn)
// 				return nil
// 			},
// 		})
// }
