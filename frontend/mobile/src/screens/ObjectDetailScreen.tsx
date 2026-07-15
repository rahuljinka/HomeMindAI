import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { Package, MapPin, Home, Layout, Box, Archive, ArrowLeft } from 'lucide-react-native';
import { useNavigation, useRoute } from '@react-navigation/native';

interface StoredObject {
  id: number;
  name: string;
  category?: string;
  description?: string;
  current_location?: {
    room: { 
      name: string;
      house?: { name: string };
    };
    furniture?: { name: string };
    container?: { name: string };
  };
  updated_at: string;
}

export default function ObjectDetailScreen() {
  const navigation = useNavigation();
  const route = useRoute();
  const { object } = route.params as { object: StoredObject };

  const location = object.current_location;

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backButton}>
          <ArrowLeft size={24} color="#000" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Object Details</Text>
      </View>

      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.card}>
          <View style={styles.objectHeader}>
            <Package size={32} color="#007AFF" />
            <View style={styles.nameContainer}>
              <Text style={styles.objectName}>{object.name}</Text>
              {object.category && <Text style={styles.categoryBadge}>{object.category}</Text>}
            </View>
          </View>

          {object.description && (
            <View style={styles.section}>
              <Text style={styles.sectionLabel}>Description</Text>
              <Text style={styles.descriptionText}>{object.description}</Text>
            </View>
          )}

          <View style={styles.section}>
            <Text style={styles.sectionLabel}>Location Hierarchy</Text>
            
            <View style={styles.hierarchyContainer}>
              {/* House */}
              <View style={styles.hierarchyItem}>
                <Home size={20} color="#666" />
                <View style={styles.hierarchyTextContainer}>
                  <Text style={styles.hierarchyLabel}>House</Text>
                  <Text style={styles.hierarchyValue}>{location?.room?.house?.name || 'Unknown'}</Text>
                </View>
              </View>
              
              <View style={styles.connector} />

              {/* Room */}
              <View style={styles.hierarchyItem}>
                <Layout size={20} color="#666" />
                <View style={styles.hierarchyTextContainer}>
                  <Text style={styles.hierarchyLabel}>Room</Text>
                  <Text style={styles.hierarchyValue}>{location?.room?.name || 'Unknown'}</Text>
                </View>
              </View>

              <View style={styles.connector} />

              {/* Furniture */}
              <View style={styles.hierarchyItem}>
                <Box size={20} color="#666" />
                <View style={styles.hierarchyTextContainer}>
                  <Text style={styles.hierarchyLabel}>Furniture</Text>
                  <Text style={styles.hierarchyValue}>{location?.furniture?.name || 'None'}</Text>
                </View>
              </View>

              <View style={styles.connector} />

              {/* Container */}
              <View style={styles.hierarchyItem}>
                <Archive size={20} color="#666" />
                <View style={styles.hierarchyTextContainer}>
                  <Text style={styles.hierarchyLabel}>Container</Text>
                  <Text style={styles.hierarchyValue}>{location?.container?.name || 'None'}</Text>
                </View>
              </View>
            </View>
          </View>

          <View style={styles.footer}>
            <Text style={styles.updatedText}>
              Last updated: {new Date(object.updated_at).toLocaleString()}
            </Text>
          </View>
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f8f9fa' },
  header: { 
    flexDirection: 'row', 
    alignItems: 'center', 
    paddingTop: 50, 
    paddingBottom: 15, 
    paddingHorizontal: 15, 
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#eee'
  },
  backButton: { padding: 5 },
  headerTitle: { fontSize: 20, fontWeight: '700', marginLeft: 15 },
  content: { padding: 15 },
  card: { 
    backgroundColor: '#fff', 
    borderRadius: 16, 
    padding: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3
  },
  objectHeader: { flexDirection: 'row', alignItems: 'center', marginBottom: 20 },
  nameContainer: { marginLeft: 15, flex: 1 },
  objectName: { fontSize: 24, fontWeight: '700', color: '#1a1a1a' },
  categoryBadge: { 
    backgroundColor: '#E3F2FD', 
    color: '#007AFF', 
    paddingHorizontal: 10, 
    paddingVertical: 4, 
    borderRadius: 12, 
    fontSize: 14, 
    alignSelf: 'flex-start',
    marginTop: 4,
    overflow: 'hidden'
  },
  section: { marginTop: 20 },
  sectionLabel: { fontSize: 14, fontWeight: '600', color: '#999', textTransform: 'uppercase', letterSpacing: 1, marginBottom: 10 },
  descriptionText: { fontSize: 16, color: '#444', lineHeight: 24 },
  hierarchyContainer: { backgroundColor: '#fdfdfd', borderRadius: 12, padding: 15, borderWidth: 1, borderColor: '#f0f0f0' },
  hierarchyItem: { flexDirection: 'row', alignItems: 'center' },
  hierarchyTextContainer: { marginLeft: 15 },
  hierarchyLabel: { fontSize: 12, color: '#999' },
  hierarchyValue: { fontSize: 16, fontWeight: '600', color: '#333' },
  connector: { width: 2, height: 15, backgroundColor: '#eee', marginLeft: 9, marginVertical: 2 },
  footer: { marginTop: 30, borderTopWidth: 1, borderTopColor: '#eee', paddingTop: 15 },
  updatedText: { color: '#999', fontSize: 12, textAlign: 'center' }
});
