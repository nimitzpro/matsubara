package main

import (
	"database/sql"
	"fmt"
	"log"
	"net/http"
	"os/exec"
	"strconv"
	"time"

	"github.com/gin-contrib/cors"
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
		// log.Fatal(err)
	}
	defer db.Close()

	var version string
	err = db.QueryRow("SELECT SQLITE_VERSION()").Scan(&version)
	if err != nil {
		// log.Fatal(err)
	}
	fmt.Println(version)

	r := gin.Default()
	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"*"},
		AllowMethods:     []string{"GET", "PUT", "PATCH"},
		AllowHeaders:     []string{"Origin"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
		AllowOriginFunc: func(origin string) bool {
			return true // origin == "https://github.com"
		},
		MaxAge: 12 * time.Hour,
	}))
	r.Use(static.Serve("/", static.LocalFile("./client/dist/", true)))
	r.NoRoute(func(c *gin.Context) {
		c.File("./client/dist/")
	})

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
	type ShortTrack struct {
		Track_uri   string
		Track_name  string
		Artist_name string
	}

	r.GET("/sql", func(c *gin.Context) {
		var track Track
		err = db.QueryRow("SELECT * FROM tracks WHERE track_name = ? COLLATE NOCASE LIMIT 1;", "Never gonna give you up").Scan(&track.Track_uri, &track.Track_name, &track.Artist_uri, &track.Artist_name, &track.Album_uri, &track.Album_name, &track.Duration_ms)
		if err != nil {
			log.Fatal(err)
		}
		c.JSONP(200, track)
	})

	r.GET("/generate", func(c *gin.Context) {
		seed_track := c.Query("seed")
		random, _ := strconv.ParseBool(c.Query("random"))
		sim, _ := strconv.ParseBool(c.Query("sim"))
		fmt.Println(c.Query("casebased"))
		casebased, _ := strconv.ParseBool(c.Query("casebased"))
		fmt.Println(casebased)
		casebased_k := c.Query("casebased_k")
		N := c.Query("length")
		var out string = ""
		if casebased {
			fmt.Println("generating case-based list off " + seed_track + "...")
			cmd := exec.Command("python", "-c", "import case; print(case.main('"+seed_track+"',"+N+","+casebased_k+"), end='')")
			fmt.Println(cmd.Args)
			o, _ := cmd.CombinedOutput()
			out += string(o) + ","
		}
		if sim {
			fmt.Println("generating sim-based list off " + seed_track + "...")
			cmd := exec.Command("python", "-c", "import sim; print(sim.main('"+seed_track+"',"+N+"), end='')")
			fmt.Println(cmd.Args)
			o, _ := cmd.CombinedOutput()
			out += string(o) + ","
		}
		if random {
			fmt.Println("generating random-based list off " + seed_track + "...")
			cmd := exec.Command("python", "-c", "import rand; print(rand.main("+N+"), end='')")
			fmt.Println(cmd.Args)
			o, _ := cmd.CombinedOutput()
			out += string(o) + "," // "{random:'" + string(o) + "'},"
		}
		if err != nil {
			fmt.Println(err)
			c.AbortWithError(500, err)
		}

		fmt.Println(string(out))
		c.JSON(200, gin.H{
			"lists": out[:len(out)-1],
		})

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

	r.GET("/search", func(c *gin.Context) {
		var tracks []ShortTrack
		// stmt, err := db.Prepare("SELECT * FROM tracks WHERE artist_name LIKE '%?%' AND track_name LIKE '%?%' LIMIT 20;")
		// if err != nil {
		// 	log.Fatal(err)
		// }
		var artist string = "%" + c.Query("artist") + "%"
		var title string = "%" + c.Query("title") + "%"
		// fmt.Println(artist + " | | " + title)
		rows, err := db.QueryContext(c, "SELECT track_uri, track_name, artist_name FROM tracks WHERE artist_name LIKE ? COLLATE NOCASE AND track_name LIKE ? COLLATE NOCASE LIMIT 20;", artist, title)
		if err != nil {
			c.AbortWithError(http.StatusInternalServerError, err)
		}
		defer rows.Close()
		for rows.Next() {
			var track ShortTrack
			if err := rows.Scan(&track.Track_uri, &track.Track_name, &track.Artist_name); err != nil {
				// if err := rows.Scan(&track.Track_uri, &track.Track_name, &track.Artist_uri, &track.Artist_name, &track.Album_uri, &track.Album_name, &track.Duration_ms); err != nil {
				// log.Fatal(err)
			}
			tracks = append(tracks, track)
		}
		if err = rows.Err(); err != nil {
			// log.Fatal(err)
		}
		c.JSONP(200, &tracks)
	})

	r.Run(":4000") // listen and serve on 0.0.0.0:8080
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
