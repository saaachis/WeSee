<?php
header('Content-Type: application/json');

try {
    // Get the data sent from the client
    $data = json_decode(file_get_contents('php://input'), true);

    if (!$data || !isset($data['imageName']) || !isset($data['imageData'])) {
        throw new Exception('Invalid JSON data.');
    }

    $imageName = $data['imageName'];
    $imageData = $data['imageData'];

    // Decode base64 image data and save it to a file
    $imageData = str_replace('data:image/png;base64,', '', $imageData);
    $imageData = str_replace(' ', '+', $imageData);
    $imageBinary = base64_decode($imageData);

    // Check if a file with the same name already exists and delete it
    if (file_exists($imageName . '.png')) {
        unlink($imageName . '.png');
    }

    // Save the new image
    $result = file_put_contents($imageName . '.png', $imageBinary);

    if ($result === false) {
        throw new Exception('Failed to save the image.');
    }

    // Send a response back to the client
    $response = array('status' => 'success');
    echo json_encode($response);
} catch (Exception $e) {
    http_response_code(500);
    $error = array('error' => $e->getMessage());
    echo json_encode($error);
    error_log('Error saving image: ' . $e->getMessage());
}
?>
