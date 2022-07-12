import {Avatar, Box, Button, Collapse, Grid, IconButton, makeStyles, Paper, Typography} from "@material-ui/core";
import React, {useState} from "react";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import SchoolIcon from '@material-ui/icons/School';

const useStyles = makeStyles(theme => ({
  card: {
    "&:hover": {
      // webkitBoxShadow: '-2px -1px 15px 7px rgba(0,0,0,0.5)',
      // mozBoxShadow: "-3px -2px 30px 14px rgba(0,0,0,0.425)",
      boxShadow: "2px 1px 5px 2px rgba(0,0,0,0.35)"
    }
  }
}))

const PublicationList = (props) => {
  const classes = useStyles();
  const {publication} = props;
  const [open, setOpen] = useState(false);
  const handleOpen = () => {
    setOpen((prevState) => !prevState);
  };

  const getRandomColor = () => {
    const colors = [
      "#303F9F",
      "#453187",
      "#A52885",
      "#F4888B",
      "#F39617",
      "#2EB2A5"
    ];
    return colors[Math.floor(Math.random() * colors.length)];
  };

  return (
    // <Box style={{}} className={classes.card}>
      <Paper className={classes.card} style={{padding: 16, marginBottom: 8}}>
        <Grid container spacing={2} onClick={handleOpen} style={{cursor: "pointer"}}>
          <Grid item xs={1}>
            <Typography variant="body2" color="textSecondary">
              {publication.year}
            </Typography>
          </Grid>
          <Grid item xs={5}>
            <Typography variant="body2" style={{fontWeight: "bold"}} color="textSecondary">
              {publication.title}
            </Typography>
          </Grid>
          <Grid item xs={5}>
            <Typography variant="body2" color="textSecondary">
              {publication.authors}
            </Typography>
          </Grid>
          <Grid item xs={1}>
            <Grid container justifyContent="flex-end">
              <Grid item>
                <IconButton disabled style={{transform: open ? "rotate(180deg)" : "", color: "inherit"}}>
                  <ExpandMoreIcon/>
                </IconButton>
              </Grid>
            </Grid>

          </Grid>
        </Grid>

        <Collapse in={open}>
          <Grid container style={{paddingBottom: 16}}>
            <Grid item xs={12} style={{paddingTop: 24, paddingBottom: 24}}>
              <Typography variant="h6"> {publication.title}</Typography>
            </Grid>
            {publication.authors.split(",").map((author) => {
              return (
                <>
                  <Grid item style={{marginBottom: 16}} xs={3}>
                    <Grid container alignItems="center">
                      <Grid item>
                        <Avatar style={{backgroundColor: getRandomColor()}}>
                          {author.split(" ")[0].charAt(0)}
                        </Avatar>
                      </Grid>
                      <Grid item xs style={{paddingLeft: 8}}>
                        <Typography> {author}</Typography>
                      </Grid>
                    </Grid>
                  </Grid>
                </>
              );
            })}
            <Grid item xs={12} style={{marginTop: 16}}>
              <Typography style={{fontWeight: "bold"}}>Abstract</Typography>
            </Grid>
            <Grid item xs={12} style={{marginTop: 8}}>
              <Typography> {publication.abstract} </Typography>
            </Grid>
            <Grid item xs={12} style={{marginTop: 32}}>
              <Button
                variant="outlined"
                color="primary"
                onClick={() => window.open(publication.url, "_blank")}
                startIcon={<SchoolIcon/>}
              >
                Semantic Scholar
              </Button>
            </Grid>
          </Grid>
        </Collapse>
      </Paper>
    // </Box>
  );
};

export default PublicationList;
