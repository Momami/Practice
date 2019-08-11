package Classes;

import java.lang.String;
import java.math.BigInteger;
import java.sql.Date;
//import java.util.Date;
import java.text.ParseException;
import java.text.SimpleDateFormat;

public class Client {
    private BigInteger IdClient;
    private String username;
    private String password;
    private Date birthOfDate;
    private String firstName;
    private String lastName;

    public Client(BigInteger IDClient, String username, String password,
                  Date birthOfDate, String firstName, String lastName) {
        this.IdClient = IDClient;
        this.username = username;
        this.password = password;
        this.birthOfDate = birthOfDate;
        this.firstName = firstName;
        this.lastName = lastName;
    }


    public BigInteger getIdClient() {
        return IdClient;
    }

    public void setIdClient(BigInteger IDClient) {
        this.IdClient = IDClient;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public Date getBirthOfDate() {
        return birthOfDate;
    }

    public void setBirthOfDate(Date birthOfDate) {
        this.birthOfDate = birthOfDate;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }
}
