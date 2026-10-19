
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  loading = false;
  errorMessage = '';
  result: any = null;

  passenger: Record<string, string | number> = {
    'Gender': 'Female',
    'Customer Type': 'Loyal Customer',
    'Age': 35,
    'Type of Travel': 'Business travel',
    'Class': 'Business',
    'Flight Distance': 1200,
    'Inflight wifi service': 4,
    'Departure/Arrival time convenient': 4,
    'Ease of Online booking': 4,
    'Gate location': 3,
    'Food and drink': 4,
    'Online boarding': 5,
    'Seat comfort': 4,
    'Inflight entertainment': 4,
    'On-board service': 4,
    'Leg room service': 4,
    'Baggage handling': 4,
    'Checkin service': 4,
    'Inflight service': 4,
    'Cleanliness': 4,
    'Departure Delay in Minutes': 0,
    'Arrival Delay in Minutes': 0
  };

  async predictSatisfaction(): Promise<void> {
    this.loading = true;
    this.errorMessage = '';
    this.result = null;

    try {
      const response = await fetch(
        'http://127.0.0.1:5000/predict',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.passenger)
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Prediction request failed.');
      }

      this.result = data;
    } catch (error) {
      this.errorMessage =
        error instanceof Error
          ? error.message
          : 'Could not connect to the Flask API.';

      this.errorMessage +=
        ' Check that the Flask server is running on port 5000.';
    } finally {
      this.loading = false;
    }
  }
}
